LEFT_WIDGET_STYLE_SHEET = '''
    QPushButton{border:none;color:white;}
    QPushButton#left_label{
        border:none;
        border-bottom:1px solid white;
        font-size:18px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
    QWidget#left_widget{
        background:gray;
        border-top:1px solid white;
        border-bottom:1px solid white;
        border-left:1px solid white;
        border-top-left-radius:10px;
        border-bottom-left-radius:10px;
    }
'''

RIGHT_WIDGET_STYLE_SHEET = '''
        QWidget#right_widget{
            color:#232C51;
            background:white;
            border-top:1px solid darkGray;
            border-bottom:1px solid darkGray;
            border-right:1px solid darkGray;
            border-top-right-radius:10px;
            border-bottom-right-radius:10px;
        }
        QLineEdit#right_bar_widget_qlinedit_input{
            border-radius: 4px;
            border: 1px solid gray;  
            height:30px;
            font-size:16px;
            font-weight:200;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QLabel#right_bar_tour_label{
            height:30px;
            font-size:16px;
            font-weight:400;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }    
        QPushButton#right_lable_title{
            border:none;
            font-size:28px;
            font-weight:700;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QPushButton#right_bar_tour_button{
            height:30px;
            border-radius: 4px;
            border: 1px solid gray;  
            font-size:16px;
            font-weight:200;
            background-color: white;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QPushButton#right_bar_tour_file_button{
            height:30px;
            border-radius: 4px;
            border: 1px solid gray;
            font-size:16px;
            font-weight:200;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QPushButton#right_bar_tour_button_download{
            height:30px;
            border-radius: 4px;
            border: 1px solid gray;  
            background-color: gray;
            font-size:16px;
            font-weight:500;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QProgressBar::chunk {
            background-color: #F76677;
        }
        QComboBox#right_bar_widget_combobox_input{
            height:30px;
            border-radius: 4px;
            border: 1px solid gray;
            font-size:16px;
            font-weight:200;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        QComboBox#right_bar_widget_combobox_enabled_input{
            height:30px;
            border-radius: 4px;
            border: 1px solid gray;
            font-color: red;
            font-size:16px;
            font-weight:1000;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
    '''