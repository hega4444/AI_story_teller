import pygame
import sys

def create_banner(image_paths, text_strings):

    # Maximum width for text
    max_text_width = 500

    # Function to split text into lines that fit within the specified width
    def split_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = words[0]
        
        for word in words[1:]:
            test_line = current_line + " " + word
            test_surface = font.render(test_line, True, (0, 0, 0))
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        lines.append(current_line)
        return lines

    # Initialize pygame
    pygame.init()

    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Movie scene creator")

    # Fill the background with black color
    screen.fill((0, 0, 0))

    # Load the images
    #image_paths = ['dataset/banana/Image_1.png', 'dataset/banana/Image_2.jpeg', 'dataset/banana/Image_3.jpg']

    images = [pygame.image.load(path) for path in image_paths]

    # Specify the desired size for the displayed images
    desired_width = 200
    desired_height = 150

    # Calculate the scaled size while maintaining the aspect ratio
    for i, image in enumerate(images):
        aspect_ratio = image.get_width() / image.get_height()
        #scaled_width = desired_width
        #scaled_height = int(desired_width / aspect_ratio)
        scaled_width = 200
        scaled_height = 150
        images[i] = pygame.transform.scale(image, (scaled_width, scaled_height))

    # Create a font
    font = pygame.font.Font(None, 24)

    # Set the positions for each image and text
    item_padding = 20
    image_rects = [
        images[0].get_rect(topleft=(item_padding, item_padding)),
        images[1].get_rect(midright=(width - item_padding, height // 2)),
        images[2].get_rect(bottomleft=(item_padding, height - item_padding))
    ]
    #text_strings = [txt1, txt2, txt3]

    text_positions = [
        (image_rects[0].topright[0]+ 10, image_rects[0].topright[1] + 10),
        (image_rects[0].bottomleft[0], image_rects[1].topleft[1] + 10),
        (image_rects[2].topright[0]+ 10, image_rects[2].topright[1] + 10)
    ]

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw the images and text
        for i, image in enumerate(images):

            screen.blit(image, image_rects[i])
     
            # Split text into lines that fit within max_text_width
            lines = split_text(text_strings[i], font, max_text_width)
            
            # Render text lines
            y = text_positions[i][1]
            for line in lines:
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(topleft=(text_positions[i][0], y))
                screen.blit(text_surface, text_rect)
                y += text_surface.get_height()

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()
    #sys.exit()
