from flask import jsonify


class Result:
    @staticmethod
    def error(code, message):
        result = {}
        result["code"] = str(code)
        result["message"] = str(message)
        return jsonify(result)

    @staticmethod
    def success(data):
        result = {}
        result["code"] = "0"
        result["message"] = "success"
        if isinstance(data, bytes):
            result["data"] = str(data, 'utf-8')
        else:
            result["data"] = data
        return jsonify(result)

    @staticmethod
    def success_similar(data, similar):
        result = {}
        result["code"] = "0"
        result["message"] = "success"
        if isinstance(data, bytes):
            result["data"] = str(data, 'utf-8')
        else:
            result["data"] = data
        if isinstance(data, bytes):
            result["similarity"] = str(similar, 'utf-8')
        else:
            result["similarity"] = similar
        return jsonify(result)