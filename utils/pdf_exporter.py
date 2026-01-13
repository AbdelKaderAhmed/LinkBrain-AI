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

    def generate_career_pdf(self, role, data):
        """
        Generates a standard single-tool report (e.g., Skill Advisor roadmap).
        """
        self.add_page()
        safe_width = 170

        # Title Section
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f"Career Roadmap: {role}", ln=True)
        self.ln(5)

        for key, value in data.items():
            if key == "error": continue
            
            # Format keys for headers
            self._draw_section_title(key.replace('_', ' ').capitalize())
            
            self.set_text_color(0, 0, 0)
            self.set_font('Helvetica', '', 11)

            if isinstance(value, list):
                for item in value:
                    # Clean text for Latin-1 compatibility
                    clean_item = str(item).encode('latin-1', 'ignore').decode('latin-1')
                    self.multi_cell(safe_width, 8, txt=f"- {clean_item}")
            else:
                clean_text = str(value).encode('latin-1', 'ignore').decode('latin-1')
                self.multi_cell(safe_width, 8, txt=clean_text)
            
            self.ln(5)

        return bytes(self.output())

    def generate_master_report(self, data_bundle):
        """
        Assembles data from all brain modules into one comprehensive PDF with Logo.
        """
        self.add_page()
        safe_width = 175
        role = data_bundle.get('role', 'Professional')

        # --- Logo Section ---
        # Note: Ensure 'logo.png' exists in your root or assets folder
        logo_path = "logo.png" 
        if os.path.exists(logo_path):
            # Placing the logo at the top left (x=10, y=10) with width=30
            self.image(logo_path, x=10, y=10, w=30)
            self.ln(15) # Add space after logo
        else:
            # Fallback if logo is missing to avoid crashing
            self.ln(10)

        # --- Report Cover ---
        self.set_font('Helvetica', 'B', 24)
        self.set_text_color(10, 102, 194) # LinkedIn Blue
        self.cell(0, 20, "Master Career Intelligence Report", ln=True, align='C')
        # --- Section 1: Profile Audit ---
        if data_bundle.get('profile'):
            self._draw_section_title("I. Profile Audit & Analysis")
            profile = data_bundle['profile']
            
            self.set_font('Helvetica', 'B', 12)
            self.set_text_color(0, 0, 0)
            self.cell(0, 10, f"Overall Profile Score: {profile.get('score', 'N/A')}/100", ln=True)
            
            self.set_font('Helvetica', '', 11)
            summary = str(profile.get('summary', '')).encode('latin-1', 'ignore').decode('latin-1')
            self.multi_cell(safe_width, 7, txt=summary)
            
            self.ln(5)
            self.set_font('Helvetica', 'B', 11)
            self.cell(0, 8, "Key Strengths:", ln=True)
            self.set_font('Helvetica', '', 11)
            for s in profile.get('strengths', []):
                self.multi_cell(safe_width, 7, txt=f"- {str(s).encode('latin-1', 'ignore').decode('latin-1')}")

        # --- Section 2: Skills & Roadmap ---
        if data_bundle.get('roadmap'):
            self._draw_section_title("II. Career Roadmap & Gap Analysis")
            roadmap = data_bundle['roadmap']
            
            self.set_font('Helvetica', '', 11)
            self.set_text_color(0, 0, 0)
            gap_text = str(roadmap.get('gap_analysis', '')).encode('latin-1', 'ignore').decode('latin-1')
            self.multi_cell(safe_width, 7, txt=gap_text)
            
            self.ln(5)
            self.set_font('Helvetica', 'B', 11)
            self.cell(0, 8, "Target Skills to Acquire:", ln=True)
            self.set_font('Helvetica', '', 11)
            for skill in roadmap.get('tech_skills', []):
                self.multi_cell(safe_width, 7, txt=f"* {str(skill).encode('latin-1', 'ignore').decode('latin-1')}")

        # --- Section 3: Networking ---
        if data_bundle.get('networking'):
            self._draw_section_title("III. Networking Strategy")
            recommendations = data_bundle['networking'].get('recommendations', [])
            
            self.set_font('Helvetica', '', 11)
            self.set_text_color(0, 0, 0)
            self.multi_cell(safe_width, 7, txt="Follow these industry leaders to expand your network:")
            self.ln(3)

            for person in recommendations:
                if "|" in person:
                    name, link, reason = person.split("|")
                    self.set_font('Helvetica', 'B', 11)
                    self.write(8, f"- {name.strip()}: ")
                    self.set_font('Helvetica', '', 11)
                    self.set_text_color(0, 0, 255)
                    self.write(8, "View Profile", link=link.strip())
                    self.set_text_color(0, 0, 0)
                    self.write(8, f" | {reason.strip()}")
                    self.ln(10)

        return bytes(self.output())