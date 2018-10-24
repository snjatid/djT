
class FormMinin:

    def get_error(self):
        if hasattr(self,"errors"):
            # <ul class="errorlist"><li>telephone<ul class="errorlist"><li>手机号太长</li></ul></li></ul>
            #print(form.errors)

            error_json = self.errors.get_json_data()
            # {'password': [{'message': '密码长度太短', 'code': 'min_length'}], 'telephone': [{'message': '手机号有点短', 'code': 'min_length'}]}     get_json_data()将上面的信息变成json

            '''
             {
                'password':
                    [
                        {'message': '密码长度太短', 'code': 'min_length'}
                    ], '
                telephone':
                    [
                        {'message': '手机号有点短', 'code': 'min_length'}
                    ]
    
                } 
    
            '''
            print(error_json)

            error_tuple = error_json.popitem()
            error_dict = error_tuple[1][0]
            # error_list = error_tuple[1]
            # error_dict = error_list[0]

            print(error_dict['message'])
            message = error_dict['message']

            return message

        return None
