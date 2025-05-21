import io
from nicegui import ui
from PIL import Image
from app.core.image_processing import analyze_skin_tone, suggest_colors, change_skin_tone

class ColorAnalyzerApp:
    def __init__(self):
        self.uploaded_image = None
        self.skin_tone = None
        self.suggested_colors = []

    def upload_image(self, file):
        if file:
            self.uploaded_image = Image.open(io.BytesIO(file))
            self.skin_tone = analyze_skin_tone(self.uploaded_image)
            self.suggested_colors = suggest_colors(self.skin_tone)
            self.update_ui()

    def change_tone(self, target_tone):
        if self.uploaded_image:
            self.uploaded_image = change_skin_tone(self.uploaded_image, target_tone)
            self.update_ui()

    def update_ui(self):
        if self.uploaded_image:
            with ui.column().classes('w-full items-center'):
                ui.image(self.uploaded_image).classes('w-64 h-64 object-cover')
                ui.label(f'Detected Skin Tone: {self.skin_tone}').classes('text-lg font-bold mt-4')
                
                with ui.row().classes('mt-4'):
                    for color in self.suggested_colors:
                        ui.button(style=f'background-color: rgb{color}; width: 50px; height: 50px;')
                
                ui.label('Change Skin Tone:').classes('mt-4')
                with ui.row().classes('mt-2'):
                    ui.button('Lighter', on_click=lambda: self.change_tone((240, 10, 10))).classes('mr-2')
                    ui.button('Darker', on_click=lambda: self.change_tone((50, 20, 20)))

@ui.page('/')
def main():
    app = ColorAnalyzerApp()
    
    ui.label('Color Analyzer for Different Skin Tones').classes('text-2xl font-bold mb-4')
    ui.upload(label='Upload Image', on_upload=app.upload_image).classes('mb-4')

ui.run()