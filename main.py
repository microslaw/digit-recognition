from display import Display
import backend as backend

input_train, input_test, labels_train, labels_test = backend.get_formated_data()

disp = Display(
    random_digit=lambda: backend.get_random_digit(input_test),
    predict=backend.predict_digit,
)

disp.main_window.mainloop()
