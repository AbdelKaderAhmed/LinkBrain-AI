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

        # --- Section 1: Profile Audit ---
        if data_bundle.get('profile'):
            self._draw_section_title("I. Profile Audit & Analysis")
            profile = data_bundle['profile']
            self.set_font('Helvetica', '', 11)
            self.multi_cell(effective_width, 7, txt=clean(profile.get('summary', '')))
            
            # Strengths & Weaknesses
            for title, key_options in [("Key Strengths", ["strengths", "Key Strengths"]), 
                                       ("Areas for Improvement", ["weaknesses", "areas_for_improvement", "Areas for Improvement"])]:
                # Try multiple possible keys
                items = []
                for k in key_options:
                    if profile.get(k):
                        items = profile.get(k)
                        break
                
                if items:
                    self.ln(3); self.set_font('Helvetica', 'B', 11); self.cell(0, 8, f"{title}:", ln=True)
                    self.set_font('Helvetica', '', 11)
                    for item in items:
                        self.set_x(20); self.multi_cell(effective_width, 6, txt=f"- {clean(item)}"); self.ln(1)

        # --- Section 2: Career Roadmap (FORCE NEW PAGE) ---
        roadmap_data = data_bundle.get('roadmap')
        if roadmap_data:
            self.add_page() # Force roadmap to start on a new page
            self._draw_section_title("II. Strategic Career Roadmap")
            
            # Handle cases where roadmap is nested or a direct dict
            content = roadmap_data.get('roadmap', roadmap_data)
            
            if isinstance(content, dict):
                for period, details in content.items():
                    self.set_font('Helvetica', 'B', 11); self.cell(0, 8, clean(period), ln=True)
                    self.set_font('Helvetica', '', 11)
                    if isinstance(details, dict):
                        # Flexibility in finding Goal/Action keys
                        goal = details.get('Objective') or details.get('Goal') or details.get('goal', '')
                        steps = details.get('Actions') or details.get('Steps') or details.get('actions', [])
                        if goal: self.multi_cell(effective_width, 6, txt=clean(f"Target: {goal}"))
                        if isinstance(steps, list):
                            for step in steps:
                                self.set_x(25); self.multi_cell(effective_width-5, 6, txt=f"* {clean(step)}")
                    else:
                        self.multi_cell(effective_width, 6, txt=clean(str(details)))
                    self.ln(4)
            else:
                self.set_font('Helvetica', '', 11)
                self.multi_cell(effective_width, 7, txt=clean(str(content)))

        # --- Section 3: Strategic Networking (FIXED SEARCH) ---
        networking_data = data_bundle.get('networking')
        if networking_data:
            # Check if we should add a page if near bottom
            if self.get_y() > 200: self.add_page()
            else: self.ln(10)
            
            self._draw_section_title("III. Strategic Networking")
            
            # Smart search for the list of people
            people_list = []
            keys_to_check = ['recommendations', 'people', 'mentors', 'network', 'top_profiles']
            for k in keys_to_check:
                if networking_data.get(k):
                    people_list = networking_data.get(k)
                    break
            
            if people_list:
                self.set_font('Helvetica', '', 11)
                for person in people_list:
                    self.set_x(20)
                    if isinstance(person, dict):
                        name = person.get('name') or person.get('Name', 'Expert')
                        link = person.get('profile_link') or person.get('link', '#')
                        reason = person.get('reason') or person.get('Reason', '')
                        self.set_font('Helvetica', 'B', 11); self.write(7, f"- {clean(name)}: ")
                        self.set_font('Helvetica', '', 11); self.set_text_color(0, 0, 255)
                        self.write(7, "LinkedIn Profile", link=link)
                        self.set_text_color(0, 0, 0); self.write(7, f" | {clean(reason)}")
                    else:
                        self.multi_cell(effective_width, 6, txt=f"- {clean(str(person))}")
                    self.ln(4)
            else:
                self.set_font('Helvetica', 'I', 11)
                self.cell(0, 8, "No networking data available in this session.", ln=True)

        return bytes(self.output())