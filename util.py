from flask import jsonify


class Result:
    @staticmethod
    def error(code, message):
        result = {"code": str(code), "message": str(message)}
        return jsonify(result)

    @staticmethod
    def success(data):
        result = {"code": "0", "message": "success"}
        if isinstance(data, bytes):
            result["data"] = str(data, 'utf-8')
        else:
            result["data"] = data
        return jsonify(result)

    @staticmethod
    def success_menu(data, menu):
        result = {"code": "0", "message": "success"}
        if isinstance(data, bytes):
            result["data"] = str(data, 'utf-8')
            result["menu"] = str(menu, 'utf-8')
        else:
            result["data"] = data
            result["menu"] = menu
        return jsonify(result)

    @staticmethod
    def success_search(data, total_number):
        result = {"code": "0", "message": "success"}
        if isinstance(data, bytes):
            result["data"] = str(data, 'utf-8')
        else:
            result["data"] = data
        if isinstance(data, bytes):
            result["totalNumber"] = str(total_number, 'utf-8')
        else:
            result["totalNumber"] = total_number
        return jsonify(result)
