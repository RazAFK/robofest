import easyocr, os, warnings, logging
warnings.filterwarnings("ignore", message=".*pin_memory.*")
logging.getLogger('easyocr').setLevel(logging.ERROR)

from robofest.settings import settings as st

class Reader:
    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(cur_dir, 'model')
        os.makedirs(model_path, exist_ok=True)

        self.reader = easyocr.Reader(['en'], gpu=False, model_storage_directory=model_path)
    
    def result(self, frame) -> tuple[list[tuple[int, int]], str, float]:
        '''
        Docstring for result
        
        :param frame: MatLike
        :param reader: reader model
        :return: 
        ret[0] = list[
            top_left(x, y),
            top_right(x, y),
            bot_left(x, y),
            bot_right(x, y)
        ]
        ret[1] = found text
        ret[2] = сonfidence
        '''
        return self.reader.readtext(frame, allowlist=st.reader_alf, )