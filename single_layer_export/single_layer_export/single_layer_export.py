from krita import *
from PyQt5.QtWidgets import QFileDialog

class single_layer_export_extension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("single_layer_export", "Export single layer", "tools/scripts")
        action.triggered.connect(self.export_trimmed_layer_to_png)

    def export_trimmed_layer_to_png(self):
        doc = Krita.instance().activeDocument()
        if not doc:
            print("No active document found.")
            return

        # Get the selected layer
        layer = doc.activeNode()
        if not layer:
            print("No layer selected.")
            return

        # Assuming only one layer is selected
        root = doc.rootNode()
        
    # Get the bounds of the selected layer
        bounds, position = layer.bounds(), layer.position()
        width, height = bounds.width(), bounds.height()

        # Create a new image with the same size as the selected layer
        new_image = Krita.instance().createDocument(width, height, "Trimmed Layer", doc.colorModel(), doc.colorDepth(), doc.colorProfile(), doc.resolution())
        
        # Remove all default layers from the new image
        for child in new_image.rootNode().childNodes():
            new_image.rootNode().removeChildNode(child)
        
        # Move the new layer to the top-left corner of the new image
        new_layer = layer.clone()
        new_layer.move(-(bounds.x() - position.x()), -(bounds.y() - position.y()))
        
        # Copy the selected layer to the new image
        new_image.rootNode().addChildNode(new_layer, None)

        # Export the new image as a PNG file
        export_path = QFileDialog.getSaveFileName(None, "Save Trimmed Layer", "", "PNG Files (*.png)")[0]
        if export_path:
            new_image.exportImage(export_path, InfoObject())

            print("Layer exported successfully.")
        print("Layer export cancelled.")

Krita.instance().addExtension(single_layer_export_extension(Krita.instance()))
