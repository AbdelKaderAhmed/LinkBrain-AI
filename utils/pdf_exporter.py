from fpdf import FPDF
import os

class PDFReport(FPDF):
    """
    PDF Generation engine for LinkBrain AI.
    Handles single reports and the Master Career Bundle.
    """

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """Sets the professional header for every page."""
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'LinkBrain AI - Professional Intelligence Report', ln=True, align='R')
        self.line(10, 18, 200, 18)
        self.ln(5)

    def footer(self):
        """Sets the footer with page numbers."""
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def _draw_section_title(self, title):
        """Helper function to create consistent blue section headers with underlines."""
        self.ln(5)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(10, 102, 194) # LinkedIn Blue
        self.cell(0, 10, title, ln=True)
        # Draw a horizontal line under the title
        self.line(self.get_x() + 10, self.get_y(), self.get_x() + 180, self.get_y())
        self.ln(5)

    def generate_master_report(self, data_bundle):
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        effective_width = 170 
        
        def clean(text):
            return str(text).encode('latin-1', 'ignore').decode('latin-1')

        # --- Header ---
        logo_path = "logo.png" 
        if os.path.exists(logo_path):
            self.image(logo_path, x=20, y=10, w=20)
            self.ln(18)
        
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(10, 102, 194) 
        self.cell(0, 10, clean("Master Career Intelligence Report"), ln=True, align='C')
        self.ln(5)

        # --- Section 1: Profile Audit ---
        if data_bundle.get('profile'):
            self._draw_section_title("I. Profile Audit & Analysis")
            profile = data_bundle['profile']
            self.set_font('Helvetica', 'B', 11); self.set_text_color(0, 0, 0)
            self.cell(0, 8, f"Score: {profile.get('score', 0)}/100", ln=True)
            self.set_font('Helvetica', '', 11)
            self.multi_cell(effective_width, 7, txt=clean(profile.get('summary', '')))
            
            # Strengths
            self.ln(2); self.set_font('Helvetica', 'B', 11); self.cell(0, 8, "Key Strengths:", ln=True)
            self.set_font('Helvetica', '', 11)
            for s in profile.get('strengths', []):
                self.set_x(20); self.multi_cell(effective_width, 6, txt=f"- {clean(s)}"); self.ln(1)

        # --- Section 2: Career Roadmap (FIXED) ---
        if data_bundle.get('roadmap'):
            self._draw_section_title("II. Career Roadmap")
            roadmap_data = data_bundle['roadmap']
            
            # Logic to handle if roadmap is a dictionary (like in your screenshot)
            self.set_font('Helvetica', '', 11)
            raw_roadmap = roadmap_data.get('roadmap', '')
            
            if isinstance(raw_roadmap, dict):
                for month, details in raw_roadmap.items():
                    self.set_font('Helvetica', 'B', 11)
                    self.cell(0, 8, clean(month), ln=True)
                    self.set_font('Helvetica', '', 11)
                    # If details is a dict, extract Objective and Actions
                    if isinstance(details, dict):
                        obj = details.get('Objective', '')
                        actions = details.get('Actions', [])
                        self.multi_cell(effective_width, 6, txt=clean(f"Objective: {obj}"))
                        if isinstance(actions, list):
                            for action in actions:
                                self.set_x(25) # Indent actions
                                self.multi_cell(effective_width - 5, 6, txt=clean(f"* {action}"))
                    else:
                        self.multi_cell(effective_width, 6, txt=clean(str(details)))
                    self.ln(2)
            else:
                self.multi_cell(effective_width, 7, txt=clean(str(raw_roadmap)))

        # --- Section 3: Networking (FIXED) ---
        if data_bundle.get('networking'):
            self._draw_section_title("III. Strategic Networking")
            net_data = data_bundle['networking']
            # Try to find the list of people in common keys like 'recommendations' or 'people'
            people = net_data.get('recommendations', []) or net_data.get('people', [])
            
            if people:
                for person in people:
                    self.set_x(20)
                    if "|" in str(person):
                        name, link, reason = str(person).split("|")
                        self.set_font('Helvetica', 'B', 11); self.write(7, f"- {clean(name.strip())}: ")
                        self.set_font('Helvetica', '', 11); self.set_text_color(0, 0, 255)
                        self.write(7, "View Profile", link=link.strip())
                        self.set_text_color(0, 0, 0); self.write(7, f" | {clean(reason.strip())}")
                    else:
                        self.set_font('Helvetica', '', 11)
                        self.multi_cell(effective_width, 6, txt=f"- {clean(person)}")
                    self.ln(8)

        return bytes(self.output())