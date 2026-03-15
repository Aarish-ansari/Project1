import os
from PIL import Image

def convert_images_to_width_zoom_a4(folder_name, output_pdf_name):
    # 1. A4 Size (300 DPI)
    A4_WIDTH = 2480
    A4_HEIGHT = 3508
    
    image_list = []
    
    try:
        if not os.path.exists(folder_name):
            print(f"Error: Folder '{folder_name}' nahi mila.")
            return

        files = sorted(os.listdir(folder_name))
        
        for filename in files:
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                img_path = os.path.join(folder_name, filename)
                img = Image.open(img_path).convert("RGB")

                # --- STEP 2: strictly Zoom to Width (2480) ---
                original_width, original_height = img.size
                
                # Nayi Height calculate karein aspect ratio ke hisaab se
                # Formula: (NewWidth / OriginalWidth) * OriginalHeight
                aspect_ratio = original_height / original_width
                new_width = A4_WIDTH
                new_height = int(A4_WIDTH * aspect_ratio)
                
                # strictly resize karein width ke barabar (Zoom ho jayega)
                img_zoomed = img.resize((new_width, new_height), Image.LANCZOS)
                print(f"Zoomed {filename} to Width: {new_width}, New Height: {new_height}")

                # --- STEP 3: A4 Canvas par adjust karna ---
                # Naya white A4 page
                a4_canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

                # --- STEP 4: Height check aur Centering ---
                if new_height > A4_HEIGHT:
                    # Agar image lambi hai, toh woh upar aur niche se thodi cut jayegi
                    # Hum center part dikhayenge
                    crop_top = (new_height - A4_HEIGHT) // 2
                    img_final = img_zoomed.crop((0, crop_top, A4_WIDTH, crop_top + A4_HEIGHT))
                    a4_canvas.paste(img_final, (0, 0))
                    print(f"Note: {filename} was too tall and was cropped centered.")
                else:
                    # Agar image chhoti hai, toh use upar/niche white margin milega (side mein nahi)
                    offset_y = (A4_HEIGHT - new_height) // 2
                    a4_canvas.paste(img_zoomed, (0, offset_y))
                
                image_list.append(a4_canvas)

        # --- STEP 5: Save PDF ---
        if image_list:
            image_list[0].save(
                output_pdf_name, 
                save_all=True, 
                append_images=image_list[1:], 
                resolution=300.0
            )
            print("-" * 30)
            print(f"SUCCESS! Zoomed PDF saved as: {output_pdf_name}")
        else:
            print("No images found in folder.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run karein
convert_images_to_width_zoom_a4("Project_2", "Zoomed_A4_Document.pdf")