"""Rock, paper, scissors game against computer using image classification done by a model trained
on machinelearningforkids.com. The program uses a pygame to create the interface, random to calculate
the computer's choice in the game, and mlforkids.py file to train the image classification model. The game is
mainly divided into two screens which are run by their own game loops. First is the welcome screen and the second is
play screen."""

# Loading required libraries
import pygame
import random
import pygame.camera
from pygame.locals import *
from mlforkids import MLforKidsImageProject

# Setup pygame and camera
pygame.init()
pygame.camera.init()

# training the machine learning model
key = "3a60b980-8ebe-11eb-9a2f-51acfbed749fc5141466-0606-47fa-b84d-5d3ab568f0cb"
image_model = MLforKidsImageProject(key)
image_model.train_model()

# Setting up window
screen = pygame.display.set_mode((720, 480))
pygame.display.set_caption('Rock, paper, scissors!')

# Setting up colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the fonts.
basicFont = pygame.font.SysFont(None, 36)


def screen_init():
    """This function sets up the screen with a white background, a vertical line in the middle, and
    two labels, namely: 'You' and 'Computer'. This function is called every time the screen is refreshed. """
    # Filling the screen with a white background
    screen.fill(WHITE)

    # Drawing a vertical line
    pygame.draw.line(screen, BLACK, (360, 0), (360, 320), 2)

    # Creating a label which says 'You'
    you_label = basicFont.render('You', True, BLACK, BLUE)
    you_label_rect = you_label.get_rect()
    you_label_rect.left = 160
    you_label_rect.top = 10
    screen.blit(you_label, you_label_rect)

    # Creating a label which says 'Computer'
    computer_label = basicFont.render('Computer', True, BLACK, RED)
    computer_label_rect = computer_label.get_rect()
    computer_label_rect.left = 480
    computer_label_rect.top = 10
    screen.blit(computer_label, computer_label_rect)


def welcome_loop():
    """This function implements the welcome screen. After initializing the screen, the camera is set up
    and images for play button and computer are put on the screen. In the loop, we create a window
    with the output from the camera which gets updated constantly. We call the play loop as soon as the play
    button is clicked."""
    screen_init()

    # Loading images on screen
    computer_image = pygame.image.load('img/computer.png')
    screen.blit(computer_image, (410, 50))
    play_button = pygame.image.load('img/play.png')
    screen.blit(play_button, (260, 380))

    # Setting up camera.
    cam = pygame.camera.Camera("/dev/video0", (320, 240))
    cam.start()

    # Main Loop
    running = True
    while running:

        # Getting new image and updating it.
        image = cam.get_image()
        screen.blit(image, (20, 50))
        pygame.display.update()

        # Iterating through the event queue.
        for event in pygame.event.get():

            # If the user presses the 'x' button in the window.
            if event.type == QUIT:
                pygame.quit()

            # If the user clicks the mouse.
            elif event.type == MOUSEBUTTONDOWN:

                # Checking the location of the mouse click and stopping camera and calling play_loop()
                if (260 < event.pos[0] < 460) and (380 < event.pos[1] < 460):
                    cam.stop()
                    play_loop()
                    running = False


def game_logic(player, computer):
    """This function takes the choices of the two players and returns the outcome of the game.

    Parameters:
        player: <str> player's choice
        computer: <str> computer's choice

    Returns:
        <str>
        """
    if player == computer:
        return "It's a tie!"
    elif player == 'rock' and computer == 'paper':
        return "Computer wins!"
    elif player == 'paper' and computer == 'scissors':
        return "Computer wins!"
    elif player == 'scissors' and computer == 'rock':
        return "Computer wins!"
    else:
        return "Player wins!"


def play_loop():
    """This function gets called every time a new game is to be played. First we load the image for the computer,
    set up the camera, and then set a timer for three seconds from the time this function gets called. Inside
    the main loop, we update the image from the camera to create a video feed. After 3 seconds, the image from
    the camera is used to tell player's choice and a random function is used to tell the computer's choice.
    We then display the result that is returned from the game_logic() function and a button to play the game
    again. """
    screen_init()

    # Loading image of the computer
    computer_image = pygame.image.load('img/computer.png')
    screen.blit(computer_image, (410, 50))

    # Setting up camera
    cam = pygame.camera.Camera("/dev/video0", (320, 240))
    cam.start()

    # Setting a timer for 3 seconds
    pygame.time.set_timer(pygame.USEREVENT, 3000, True)

    # Creating a list of choices for the computer to choose from.
    choices = ['rock', 'paper', 'scissors']

    # Main loop
    running = True
    while running:

        # Getting new image and updating it
        image = cam.get_image()
        screen.blit(image, (20, 50))
        pygame.display.update()

        # Iterating through the event queue
        for event in pygame.event.get():

            # If the user presses the 'x' button in the window
            if event.type == QUIT:
                pygame.quit()

            # When the 3 second timer runs out
            elif event.type == pygame.USEREVENT:

                # Capturing image, classifying it, and displaying the result
                pygame.image.save(image, 'img/result_image.png')
                result = image_model.prediction('img/result_image.png')
                result_label = basicFont.render(result['class_name'], True, BLACK, BLUE)
                result_label_rect = result_label.get_rect()
                result_label_rect.left = 160
                result_label_rect.top = 300
                screen.blit(result_label, result_label_rect)

                # Making a random choice for the computer and displaying it
                computer_result = random.choice(choices)
                computer_result_label = basicFont.render(computer_result, True, BLACK, RED)
                computer_result_label_rect = computer_result_label.get_rect()
                computer_result_label_rect.left = 500
                computer_result_label_rect.top = 300
                screen.blit(computer_result_label, computer_result_label_rect)

                # Displaying the result of the game
                winner = game_logic(result['class_name'], computer_result)
                winner_label = basicFont.render(winner, True, BLACK, GREEN)
                winner_label_rect = winner_label.get_rect()
                winner_label_rect.left = 260
                winner_label_rect.top = 340
                screen.blit(winner_label, winner_label_rect)

                # Creating a play again button
                play_again_button = pygame.image.load('img/play again.png')
                screen.blit(play_again_button, (260, 380))

            # If the user clicks the mouse
            elif event.type == MOUSEBUTTONDOWN:

                # Restarting game if the user has clicked on play again button
                if (260 < event.pos[0] < 460) and (380 < event.pos[1] < 460):
                    cam.stop()
                    play_loop()
                    running = False


# Starting the game
welcome_loop()
