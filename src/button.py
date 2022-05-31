

class Button:

    def __init__(self, image, hovered_img, pos, base_color=None, hovering_color=None, text_input=None, font=None):
        self.image = image
        self.hovered = hovered_img
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        if text_input:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        self.cur_image = image

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.cur_image, self.rect)
        if self.text_input:
            screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(
                self.rect.top, self.rect.bottom):
            return True
        return False

    def change_bg(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(
                self.rect.top, self.rect.bottom):
            # self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.cur_image = self.hovered
        else:
            # self.text = self.font.render(self.text_input, True, self.base_color)
            self.cur_image = self.image
