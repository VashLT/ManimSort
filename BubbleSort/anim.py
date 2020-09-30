from manim import *
import shutil


def compute_scale_factor(scaler):
    assert scaler >= 1
    new_scale = 1 - (scaler - 1)
    return new_scale


class Sort(VGroup):
    CONFIG = {
        "inner_text_style": {
            "color": WHITE,
            "stroke_width": 1
        },
        "boxes_style": {
            "stroke_color": BLUE,
            "stroke_width": 4
        },
        "blocks_buff": 0.03,
        "swapping_config": {
            "indicate_color": GREEN,
            "scale_factor": 1.02,
            "shift": UP*2,
            "rate_func": linear
        }
    }

    def __init__(self, iterable, **kwargs):
        super().__init__(**kwargs)
        self.digest_iterable(iterable)
        self.scale_to_match()

    def get_block(self, index):
        try:
            if not hasattr(self, "position_ref"):
                raise Exception(
                    "[ERROR] Cannot use this method without -position_ref- attr.")
            element = self.input[index]
            return self.position_ref[element]
        except IndexError:
            print(
                f"[ERROR] {index} is not a valid index. Iterable size: {len(self.input)} elements")
        except KeyError:
            print(f"[ERROR] Wrong key - {element}")

    def digest_iterable(self, iterable):
        self.input = iterable
        widest = max(iterable)
        # based on max number, create rectangles with the same width
        sample = SurroundingRectangle(
            MathTex(str(widest)), buff=.2)
        for inner in iterable:
            block = self.build_block(inner, sample)
            self.add(block)
        self.arrange_submobjects(buff=self.blocks_buff)
        self.keep_place_according_to_iter()

        self.restore_color = self[0].get_color()

        blocks = self.copy()
        [self.add(block.value) for block in blocks]

    def build_block(self, insider, model):
        text = MathTex(str(insider), **self.inner_text_style)
        box = model.copy().set_style(**self.boxes_style)
        box.value = text
        self.keep_track(text, box)
        return box

    def keep_place_according_to_iter(self):
        self.position_ref = {}  # key-value pairs like key: input_element, value: coord
        assert hasattr(self, "input")
        for element, mob in zip(self.input, self):
            self.position_ref.setdefault(element, mob)
            # mob.item = element

    def keep_track(self, mob1, mob2):
        def update_mob(m):
            m.move_to(mob2.get_center())
        mob1.add_updater(update_mob)

    def scale_to_match(self):
        n = len(self.input)
        proportion = 0.7
        factor = (Camera().frame_width * proportion) / n
        self.scale(factor)

    def swap_elements(self, index_el1, index_el2, animate=False, **kwargs):
        """ given two index to respective elements swap them in the input iterable"""
        try:
            cache = self.input[index_el1]
            self.input[index_el1] = self.input[index_el2]
            self.input[index_el2] = cache
            # swap input iterable elements
            if animate:
                mob1 = self.position_ref[cache]
                mob2 = self.position_ref[self.input[index_el1]]
                return self.swap_animation(mob1, mob2, **kwargs)

        except IndexError:
            print(
                f"[ERROR] Given indexes are not valid. Iterable size: {len(self.input)} elements")

    def swap_animation(self, mob1, mob2, **kwargs):
        """ """
        merge_dicts_recursively(self.swapping_config, kwargs)
        ref_positions = [mob1.copy().get_center(), mob2.copy().get_center()]
        restore_scale_factor = compute_scale_factor(
            self.swapping_config["scale_factor"])
        anims = [
            [mob1.set_color, self.swapping_config["indicate_color"],
             mob1.scale, self.swapping_config["scale_factor"],
             mob2.set_color, self.swapping_config["indicate_color"],
             mob2.scale, self.swapping_config["scale_factor"]],
            [mob1.shift, self.swapping_config["shift"],
             mob2.shift, self.swapping_config["shift"]],
            [mob1.move_to, ref_positions[1],
             mob1.scale, restore_scale_factor,
             mob1.set_color, self.restore_color,
             mob2.move_to, ref_positions[0],
             mob2.scale, restore_scale_factor,
             mob2.set_color, self.restore_color],
        ]
        return anims


class Sorting(Scene):
    CONFIG = {
        "iterating_config": {
            "stay_element_color": YELLOW,
            "iter_elements_color": PURPLE,
            "scale_factor": 1.03
        }
    }

    def construct(self):
        name = Tex("BubbleSort").scale(
            1.4).set_color_by_gradient([WHITE, GRAY, BLUE])
        name.to_edge(UP, buff=1)
        n = np.random.randint(1, 200)
        to_sort = np.random.randint(1, 10000, size=n, dtype=np.int64)

        sort = Sort(to_sort).shift(DOWN)
        self.play(
            ShowCreation(sort),
            AnimationGroup(
                Pause(3.1),
                ShowCreation(name), lag_ratio=1
            ), run_time=4)
        self.add(sort)
        self.sort_iterable_anim(sort)
        self.wait(2)

    def sort_iterable_anim(self, mob_array, indicate_color=RED):
        array = mob_array.input
        time = 0.2
        n = len(array)
        should_restore = True
        restore_scale_factor = compute_scale_factor(
            self.iterating_config["scale_factor"])
        restore_color = mob_array[0].get_color()
        for i in range(n):
            self.add_foreground_mobject(mob_array[i])
            self.play(
                mob_array.get_block(
                    i).set_color, self.iterating_config["stay_element_color"],
                mob_array.get_block(
                    i).scale, self.iterating_config["scale_factor"], run_time=time
            )
            should_restore = True
            for j in range(i + 1, n, 1):
                # anim
                self.add_foreground_mobject(mob_array.get_block(j))
                self.play(
                    mob_array.get_block(
                        j).set_color, self.iterating_config["iter_elements_color"],
                    mob_array.get_block(
                        j).scale, self.iterating_config["scale_factor"], run_time=time
                )
                self.play(
                    mob_array.get_block(j).set_color, restore_color,
                    mob_array.get_block(j).scale, restore_scale_factor
                )
                self.remove_foreground_mobject(mob_array.get_block(j))
                ################
                if array[i] >= array[j]:
                    # restore the mob before swaping it
                    self.play(
                        mob_array.get_block(i).set_color, restore_color,
                        mob_array.get_block(i).scale, restore_scale_factor
                    )
                    anims = mob_array.swap_elements(i, j, animate=True)
                    for anim in anims:
                        self.play(
                            *list(anim), run_time=1
                        )
                    self.play(
                        mob_array.get_block(
                            i).set_color, self.iterating_config["stay_element_color"],
                        mob_array.get_block(
                            i).scale, self.iterating_config["scale_factor"], run_time=time
                    )

            self.play(
                mob_array.get_block(i).set_color, restore_color,
                mob_array.get_block(i).scale, restore_scale_factor
            )
            self.remove_foreground_mobject(mob_array.get_block(i))
        # return anims


def del_folder():
    path = os.path.join(os.getcwd(), "media", "videos", "anim")
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


def main():
    # for creation purposes
    del_folder()
    os.system(r"manim .\Python\Algorithms\ManimSort\Bubble\anim.py Sorting -p")


if __name__ == "__main__":
    main()
