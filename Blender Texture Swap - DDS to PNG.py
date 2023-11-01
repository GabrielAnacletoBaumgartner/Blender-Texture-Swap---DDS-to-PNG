import bpy
import os
import numpy as np


# Options:

ClearConsole = True
debug0 = False
debug1 = False
debug2 = False
debug3 = False
debug4 = False
debug5 = False
dupmaxcheck = 1000 # Max number of duplicates the script will check (If 1000, it will check from 0.001 up to 1.000)
subfolder = "" #If you want your textures to be in your root folder (where your .blend file is located), keep it as it is. If you want to add subfolder like "Assets/Textures", so your textures will be saved in "%RootFolder%/Assets/Textures", replace it by "Assets/Textures" or "Assets\Textures"
RemoveDDSs = True # Removes DDS files from the project.


# Var definitions:

dupbreaker = 0
PngVariant = 0


# Code start here:

if (ClearConsole == True): # As the name suggests it clears the console if ClearConsole is active.
    os.system('cls')

# Directory Stuff:

ProjectPath = bpy.data.filepath # As the name suggests, it save the project path (the path to your .blend file) to "ProjectPath" variable.
ProjectName = bpy.path.basename(bpy.context.blend_data.filepath) #As the name suggests, it save the name of your .blend file to "ProjectName" variable.
ProjectNameLength = len(ProjectName) # It calulates the ammount of characters (uncluding space and file extension), present in your project file name.
RootDir = ProjectPath[:-(ProjectNameLength)] #
subfolder = subfolder.replace("/","\\")

if (debug0 == True):
    print("..........debug0..........")
    print("ProjectPath is:", ProjectPath)
    print("ProjectName is:", ProjectName)
    print("ProjectNameLength is:", ProjectNameLength)
    print("RootDir is:", RootDir)
    print("subfolder is:", subfolder)
    print("..........debug0..........")
    print("")

#Saved project verifier:
    
if (ProjectPath == None)or(ProjectPath == 0)or(ProjectPath == ""): # If project is not saved print this message.
    print("...................")
    print("....Save before....")
    print("....running the....")
    print("......script.......")
    print("...................")
    print("")
else: # If it is, then run the script.
    
    importmat = bpy.data.materials.get("Importer")
    # Define importmat variable as a material named Importer, if Importer already exist.
    
    if importmat is None:
        importmat = bpy.data.materials.new(name="Importer")
    # If the Importer material does not exist, create it.
    
    importmat.use_nodes = True # Make importmat use nodes.
    texImage = importmat.node_tree.nodes.new('ShaderNodeTexImage') # Makes texImage a texture variable to import new textures.
    
    for img in bpy.data.images:
        if (img.name != "Render Result")and(img.name != "Viewer Node"): # Removes Render Result and Viewer Node from the images being processed.
            
            imgnamecache = img.name # Caches the image name to avoid "python weirdness" (Just keep as it is, really).
            imgsuffix = imgnamecache[-4:]
#            pngpath = RootDir+subfolder+imgnamecache
            if (debug1 == True): # Print the cached image name if debug1 is active.
                print("..........debug1..........")
                print("Cached name is:", imgnamecache)
                print("Cached image name has ", imgsuffix, "as suffix.")
                #print("Pngpath is:", pngpath)
                print("..........debug1..........")
                print("")
            
            for dupcounter in np.arange(0, dupmaxcheck, 1): # Verifies from 0 to the valued defined in "dupmaxcheck" for duplicates an increases dupbreaker by 1.
                dupsuffix = "{:03d}".format(dupcounter) # Saves the current dupcounter formated with 3 caracters to dupsuffix variable.
                dupsuffix = ("."+dupsuffix) # Add the point before the value, making it a decimal (Using decimals with "for" directly would result in floating numbers and a giant "code witchcraft" to fix it).
                if (imgsuffix ==  dupsuffix): # Verifies if the image suffix is equal to a duplicate suffix and if it is, increase "dupbreaker" by 1.
                    dupbreaker = dupbreaker+1
                    if (debug2 == True): # Prints the message below for duplicates if debug2 i active.
                        print("..........debug2..........")
                        print("Duplicate found.")
                        print("..........debug2..........")
                        print("")
            
            for img in bpy.data.images: # Verifies if there's a png variant already.
                if (img.name != "Render Result")and(img.name != "Viewer Node"): # Removes Render Result and Viewer Node from the images being processed.
                    if (imgnamecache[-4:] != (".png"))and(imgnamecache[:-4]+(".png") == img.name): # If the "imgnamecache" (current image being processed) is not a PNG and if the current image have a png equivalent execute the commands below.
                        PngVariant = PngVariant+1 # Add 1 to "PngVariant"
                        if (debug3 == True):
                            print("..........debug3..........")
                            print(PngVariant, "PNG variant(s) found")
                            print(imgnamecache, "PNG variant is", img.name)
                            print("..........debug3..........")
                            print("")

            if (dupbreaker == 0)and(PngVariant == 0): # Only execute the commands below if it's not a duplicate (It uses "dupbreaker" to verify it) And if there's no png variant already loadeed (It uses "PngVariant" to verify it).
                if (imgsuffix == ".dds"): #Removes Non .dds images from the execution.
                    pngpath = RootDir+subfolder+(imgnamecache.replace(".dds",".png")) # Build the new png path using the Root Foolder, subfolder, .dds image name, and replaces the extension by .png (Basically creating the new .png directory)
                    texImage.image = bpy.data.images.load(pngpath)
                    if (debug4 == True):
                        print("..........debug4..........")
                        print("Cached name is:", imgnamecache)
                        print("Cached image name has ", imgsuffix, "as suffix.")
                        print("Breaks?", dupbreaker)
                        print("Pngpath is:", pngpath)
                        print("..........debug4..........")
                        print("")

            PngVariant = 0 # After running the commands, reset "PngVariant" value to use it again in the next image check.    
            dupbreaker = 0 # After running the commands, reset "dupbreaker" value to use it again in the next image check.
    
    img.reload() # Reloads? (:P)
    
    bpy.data.materials.remove(importmat) # After running the script removes the Importer material to keep everything clean.

    for ob in bpy.data.objects: #for each ob
        if ob.type == "MESH": #of "mesh" type
            for mat_slot in ob.material_slots: #for each mat_slot of these objects
                if mat_slot.material:  #if mat_slot is a material
                    if mat_slot.material.node_tree: #if mat_slot is a material with node tree
                        for x in mat_slot.material.node_tree.nodes:
                            if x.type=='TEX_IMAGE': #set x as the image/texture node
                                imagestring = str(x.image.name) # Store the texture name into a string and replace it's the extension by .png
                                if (imagestring[-4:] == ".dds"): # Process only .DDS images.
                                    imageobj = bpy.data.images.get(imagestring.replace('.dds', '.png'), None) # Get the png image by it's name and store it into a image variable
                                    x.image = imageobj # Replace the dds image by the png image.
                                    if (debug5 == True):
                                        print("texture dds: "+str(x.image.name))
                        if (debug5 == True):
                            print("material:" + str(mat_slot.material.name))                

    if (RemoveDDSs == True): #If the RemoveDDSs was set to True, it will remove all the DDS images from the project.
        for img in bpy.data.images:
            if (img.name[-4:] == ".dds"):
                bpy.data.images.remove(img)

    print("..................")
    print(".......Done.......")
    print("..................")
    print("")