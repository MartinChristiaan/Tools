from library.sub_library import my_sum, ObjectExample


def main():
    my_sum(2, 3, mode="test")
    my_sum(3, 3, mode="test")
    my_sum(4, 3, mode="test")
    my_sum(2, 3, mode="test")
    my_sum(6, 3, mode="test")
    obj = ObjectExample(2, 4)

    img = obj.generate_test_image()
    obj.process_test_image(img)
    obj.do_sum_exception()
    print("executing the remainder of the script")
