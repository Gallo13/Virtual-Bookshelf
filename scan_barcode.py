# Created by: Jess Gallo
# Date Created: 10/13/2024
# Last Modified: 10/13/2024
# Description:

from barcode_scanner import *
from get_data import *

scan_barcode_routes = Blueprint('scan_barcode', __name__)


@scan_barcode_routes.route('/scan_barcode', methods=['GET', 'POST'])
def scan_barcode():
    print('You clicked the barcode')
    if request.method == 'POST':
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        barcode_read = False
        while ret and not barcode_read:
            ret, frame = camera.read()
            frame, barcode_read, isbn = read_barcode(frame)
            cv2.imshow('Real Time Barcode Scanner', frame)
            if barcode_read:
                print("ISBN: ", isbn)
                break
            elif cv2.waitKey(1) & 0xFF == 27:
                break

        camera.release()
        cv2.destroyAllWindows()
    return render_template('login.html')
