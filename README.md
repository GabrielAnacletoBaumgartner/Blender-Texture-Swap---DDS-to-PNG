# Blender-Texture-Swap---DDS-to-PNG

- Description

This is my first python code.

It has an Options sections.
The most relevant ones are subfolder and RemoveDDSs.
To swap the textures, first use an external software like "Photoshop's Image Processor PRO" to batch process and convert all dds textures to png.
Changing the name of the png variant to something different will result in a script error.
This first version does not convert the textures and also does not check if there is a png variant.

I decided to create this script while edditing some models that had dds textures and for some reason, sometimes DDS files do not load in my Blender.

- Usage

After loading a model in Blender with a dds texture, save the project and convert the dds textures to png.
Move the png Textures to the root folder (Where your .blend file was saved), or the subfolder inside it if you defined a subfolder in the Options section.
In Blender's "Text Editor" (Shift + F11) open the script.
Click run (or press Alt + P).

- TO DO LIST:

Verify existance system.
Convert option.
