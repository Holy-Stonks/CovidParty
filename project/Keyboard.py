from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard:

    TRAIN = 'train'

    @staticmethod
    def createKeyboard(response):
        keyboard = VkKeyboard(one_time=True)

        if response == Keyboard.TRAIN:
            keyboard = Keyboard.trainKeyboard(keyboard)

        return keyboard.get_keyboard()

    @staticmethod
    def trainKeyboard(keyboard):
        keyboard.add_button("Зарядка", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button("Йога", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("Назад", color=VkKeyboardColor.DEFAULT)
        return keyboard
