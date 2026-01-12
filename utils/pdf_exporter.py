from fpdf import FPDF

class PDFReport(FPDF):
    """
    Ultra-stable layout: Forces X-coordinate reset to prevent horizontal drifting.
    """
    
    def __init__(self):
        # A4 is 210mm wide. 
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(left=20, top=20, right=20)
        self.set_auto_page_break(auto=True, margin=20)
        self.set_font("Helvetica", size=12)

    def header(self):
        """Standard Header with explicit X reset."""
        self.set_x(20) # Force start at left margin
        self.set_font('Helvetica', 'B', 15)
        self.cell(170, 10, 'LinkBrain AI - Career Report', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

    def generate_career_pdf(self, role, data):
        """
        Generates content with forced left-alignment (set_x) for every section.
        """
        self.add_page()
        
        # Use 170mm as a safe fixed width (210mm total - 40mm margins)
        safe_width = 170

        # Section: Role Title
        self.set_x(20) 
        self.set_font('Helvetica', 'B', 14)
        self.multi_cell(safe_width, 10, txt=f"Professional Roadmap: {role}")
        self.ln(5)

        for key, value in data.items():
            if key == "error": continue
            
            # Reset X to 20mm for every Header
            self.set_x(20)
            self.set_font('Helvetica', 'B', 12)
            title = key.replace('_', ' ').capitalize()
            self.multi_cell(safe_width, 10, txt=f"{title}:")
            
            # Reset X to 20mm for every Content block
            self.set_font('Helvetica', '', 11)
            if isinstance(value, list):
                for item in value:
                    self.set_x(25) # Slightly indented for bullets
                    safe_item = str(item).encode('latin-1', 'ignore').decode('latin-1')
                    self.multi_cell(safe_width - 5, 8, txt=f"- {safe_item}")
            else:
                self.set_x(20)
                safe_text = str(value).encode('latin-1', 'ignore').decode('latin-1')
                self.multi_cell(safe_width, 8, txt=safe_text)
            
            self.ln(5)

        return bytes(self.output())