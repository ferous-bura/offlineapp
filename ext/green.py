from PIL import Image, ImageDraw, ImageFont
import os
from list_1_150 import hagere_bingo

# Define the folder where images should be saved
output_folder = "bingo_cards"

# Ensure the folder exists (create it if it doesn't)
os.makedirs(output_folder, exist_ok=True)

# Define card and grid sizes for 300 PPI output (22 cm * 300 PPI / 2.54 cm per inch ≈ 2598 pixels)
card_size = int(22 * 300 / 2.54)  # Approximately 2598 pixels
header_height = card_size // 10  # 10% of card height for header
footer_height = header_height * 2  # Footer height twice the header height
grid_area_height = card_size - (header_height + footer_height)  # Remaining space for grid

# Define cell dimensions within grid area
cell_width = card_size // 5  # Width per cell
cell_height = grid_area_height // 5  # Smaller height per cell
grid_size = 5

# Create a function to generate a Bingo card image
def generate_bingo_card(numbers, card_number):
    # Create base image at 300 PPI with a greyish background
    img = Image.new('RGB', (card_size, card_size), color=(200, 200, 200))  # Greyish background
    draw = ImageDraw.Draw(img)

    # Set up fonts for header, numbers, and footer
    header_font = ImageFont.truetype("arialbd.ttf", 150)  # Larger bold font for "BINGO"
    number_font = ImageFont.truetype("arial.ttf", 250)  # Larger font for numbers
    footer_font = ImageFont.truetype("NotoSansEthiopic.ttf", 180)  # Amharic font for footer
    footer_number_font = ImageFont.truetype("arialbd.ttf", 320)  # Bold and larger footer number font

    # Draw header with "BINGO" text in teal background, aligning each letter in its column
    draw.rectangle([0, 0, card_size, header_height], fill="blue")
    bingo_text = "BINGO"

    # Calculate x position for each letter to center it in each column
    for col in range(grid_size):
        letter = bingo_text[col]
        letter_x = col * cell_width + (cell_width - draw.textbbox((0, 0), letter, font=header_font)[2]) / 2
        draw.text((letter_x, (header_height - header_font.size) / 2), letter, fill="white", font=header_font)

    # Draw footer with "ካርቴላ ቁጥር." and card number within the allocated footer space
    footer_y = card_size - footer_height
    draw.rectangle([0, footer_y, card_size, card_size], fill="silver")  # Footer background

    # Define footer text and number
    footer_text = "ብሬ ቢንጎ"
    footer_number_text = f"{card_number}"

    # Calculate positions
    footer_text_x = (card_size - draw.textbbox((0, 0), footer_text, font=footer_font)[2]) / 2  # Center the "Cartella No." text
    footer_number_x = card_size - draw.textbbox((0, 0), footer_number_text, font=footer_number_font)[2] - 160  # Offset the number 10 pixels from the right edge

    # Draw the texts
    draw.text((footer_text_x, footer_y + (footer_height - footer_font.size) / 2), footer_text, fill="black", font=footer_font)

    # Fixed height for footer number
    footer_number_y = footer_y + 150  # Adjust this value to set the fixed vertical position
    draw.text((footer_number_x, footer_number_y), footer_number_text, fill="blue", font=footer_number_font)

    # Draw "wende" in the top-left corner
    wende_font = ImageFont.truetype("arialbd.ttf", 50)  # Font size for "wende"
    draw.text((10, 10), "maya", fill="black", font=wende_font)

    # Draw a decorative circle around the footer number
    number_width, number_height = draw.textbbox((0, 0), footer_number_text, font=footer_number_font)[2:]
    circle_radius = max(number_width, number_height) // 2 + 10  # Radius based on the size of the number with some padding
    circle_x = footer_number_x + (number_width // 2) - circle_radius
    circle_y = footer_number_y - circle_radius + (number_height // 2)  # Center the circle vertically around the number
    #draw.ellipse([circle_x, circle_y, circle_x + 2 * circle_radius, circle_y + 2 * circle_radius], outline="black", width=15)

    # Underline for "Cartella No."
    underline_y = footer_y + (footer_height - footer_font.size) / 2 + footer_font.size + 5  # Position below the text
    underline_length = draw.textbbox((0, 0), footer_text, font=footer_font)[2]  # Length of the underline
    #draw.line((footer_text_x, underline_y, footer_text_x + underline_length, underline_y), fill="black", width=3)  # Draw the underline

    # Draw grid and populate with numbers with thicker borders and bump effect
    for i, number in enumerate(numbers):
        x = (i % grid_size) * cell_width
        y = header_height + (i // grid_size) * cell_height
        text = "free" if number == 0 else str(number)

        # Apply a bump effect by shifting the number slightly
        bump_offset = 26  # Change this for more or less bump effect
        text_width, text_height = draw.textbbox((0, 0), text, font=number_font)[2:]
        text_x = x + (cell_width - text_width) / 2 + bump_offset
        text_y = y + (cell_height - text_height) / 2 - bump_offset

        draw.text((text_x, text_y), text, fill="black", font=number_font)

        # Draw thick borders around each cell
        # draw.rectangle([x, y, x + cell_width, y + cell_height], outline="teal", width=32)
        # Draw rounded borders around each cell
        corner_radius = 40  # Adjust this value for more or less roundness
        draw.rounded_rectangle([x, y, x + cell_width, y + cell_height], radius=corner_radius, outline="blue", width=24)

    # Save the image at 300 DPI
    #img.save(f"bingo_card_{card_number}.jpg", dpi=(300, 300))
    img.save(os.path.join(output_folder, f"bingo_card_{card_number}.jpg"), dpi=(300, 300))

# Loop through each line of Bingo numbers and generate a card
for i, line in enumerate(hagere_bingo):
    generate_bingo_card(line, i + 1)
