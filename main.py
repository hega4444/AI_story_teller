import openai  # importing the almighty openai library
from key_api import KEY
from imager import ImageDownload
from banner import create_banner
import os

# Make sure to set up your API key
openai.api_key = KEY


def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


# USING AI TO GET RESPONSE
def get_chatgpt_response(user_input, completions: int):
    response = openai.Completion.create(
        engine="text-davinci-003",  # choosing model of openai's AI
        prompt=user_input,  # choosing what to use for prompting
        max_tokens=150,  # limit the maximum response tokens
        temperature=0.7,  # choosing temperature (more random/creative here)
        n=completions,  # modifiable completion number
        best_of=3,  # Generates n * best_of completions and returns the best n.
        echo=True,  # Return the user's input in the response
        presence_penalty=0.5,  # higher value = more likely to introduce new topics
        frequency_penalty=0.5,  # higher value = more likely to repeat information
    )
    choices = []
    for i in range(completions):
        choices.append(response.choices[i].text.strip())
    return choices


class Story:
    def __init__(self, movie_name) -> None:
        input = (
            "Based on the movie"
            + movie_name
            + """, return a python list named output with first three elements the names
of characters belonging to a specific scene of that movie, and the fourth 
element a brief plot of the scene. Do not use the ' symbol, instead ´ """
        )
        response = get_chatgpt_response(input, 1)

        # Extract the content within the list and remove the outermost brackets
        list_content = response[0].split("[", 1)[1].rsplit("]", 1)[0]

        #print(list_content)
        
        # Convert the content into a real Python list using eval()
        output_list = eval(list_content)

        self._names = output_list[0:3]
        self._plot = output_list[3]
        self._movie_name = movie_name

        print("\nCharacters:\n", self._names)
        print("\nPlot:\n", self._plot)

        self._characters = []
        self._super = []

    def create_characters(self):
        for name in self._names:
            new_character = Character(name, self._plot)
            self._characters.append(new_character)

    def create_fun_characters(self):
        for name in self._names:
            new_super = SuperCharacter(name, self._plot)
            self._super.append(new_super)

    def make_them_talk(self):
        imgs = []
        txts = []
        for actor in self._characters:
            img = ImageDownload(self._movie_name + " " + actor._name)
            imgs.append(img.path)

            txts.append(actor.say_line())

        create_banner(imgs, txts)

    def make_them_talk_funny(self):
        imgs = []
        txts = []
        for actor in self._super:
            img = ImageDownload(self._movie_name + " " + actor._name)
            imgs.append(img.path)

            txts.append(actor.tell_joke())

        create_banner(imgs, txts)


class Character:
    def __init__(self, name, plot) -> None:
        self._name = name
        self._plot = plot
        input = (
            "you are "
            + name
            + " in this context:"
            + plot
            + ". Say something appropiate to the context and interact with the other characters."
        )
        response = get_chatgpt_response(input, 1)

        # Extract the last part after the last newline character
        self._quote = response[0].rsplit("\n", 1)[-1].strip()

    def say_line(self):
        return self._name + " says: " + self._quote


class SuperCharacter(Character):
    def __init__(self, name, plot) -> None:
        super().__init__(name, plot)
        input = (
            "you are "
            + name
            + " in this context:"
            + plot
            + ". Make a joke of the situation."
        )
        response = get_chatgpt_response(input, 1)

        # Extract the last part after the last newline character
        self._joke = response[0].rsplit("\n", 1)[-1].strip()

    def tell_joke(self):
        return self._name + " says: " + self._joke


clear_screen()
print("***Story creator***\n")
new_movie = Story(input("Please indicate the name of a movie to recreate a scene:"))

print("\nCreating Scene script, please wait...")
new_movie.create_characters()
new_movie.make_them_talk()

if input("\nWant to read the fun version of this scene?[y/n]:").lower() == "y":
    print("\nCreating Scene script, please wait...")
    new_movie.create_fun_characters()
    new_movie.make_them_talk_funny()
