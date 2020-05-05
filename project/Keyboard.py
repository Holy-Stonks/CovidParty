from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard:

    TRAIN = 'train'
    EXERCISE = 'exercise'

    @staticmethod
    def createKeyboard(response):
        keyboard = VkKeyboard(one_time=True)

        if response == Keyboard.TRAIN:
            keyboard = Keyboard.trainKeyboard(keyboard)
        elif response == Keyboard.EXERCISE:
            keyboard = Keyboard.exerciseKeyboard(keyboard)

        return keyboard.get_keyboard()

    @staticmethod
    def trainKeyboard(keyboard):
        keyboard.add_button("Зарядка", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button("Йога", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("Назад", color=VkKeyboardColor.DEFAULT)
        return keyboard

    @staticmethod
    def exerciseKeyboard(keyboard):
        keyboard.add_button("Упражнение", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button("Случайная музыка", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("Выйти", color=VkKeyboardColor.DEFAULT)
        return keyboard
