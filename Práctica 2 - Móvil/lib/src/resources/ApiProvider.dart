import 'dart:convert';
import 'dart:io';

import 'package:iagram/src/models/imgresponse.dart';
import 'package:http/http.dart' as http;

class ApiProvider {
  static const String API_ENDPOINT_URL = 'https://api.imagga.com/v2/tags';
  static const String API_AUTH = 'Basic YWNjXzczNDY0MGE0ZDk1ZjNhMjowOTFmZjdmZDg0MDVkY2MxZjk2NDNmMzE1Nzg2NGI1YQ==';

  Future<ResponseModel> getTags(File image) async{

    http.MultipartRequest request = http.MultipartRequest(
      'POST',
      Uri.parse(ApiProvider.API_ENDPOINT_URL),
    );

    Map<String, String> headers = {
      "Connection": "Keep-Alive",
      "Cache-Control": "no-cache",
      "Content-Type": "multipart/form-data",
      "Authorization": ApiProvider.API_AUTH,
    };

    request.headers.addAll(headers);
    request.fields["language"] = "en,es";
    //Por si se quiere limitar el número de tags
    //Por defecto salen entre 80 y 120, según la foto
    //request.fields["limit"] = "30";

    request.files.add(
      http.MultipartFile.fromBytes(
        'image',
        image.readAsBytesSync(),
      ),
    );

    http.StreamedResponse response = await request.send();
    print("Response status code: " + response.statusCode.toString());

    if (response.statusCode == 200){
      String responseJson = await response.stream.bytesToString();
      print(responseJson);
      return ResponseModel.fromJson(jsonDecode(responseJson));
    }
    return new ResponseModel(null, new Status("HTTP ERROR: ", response.statusCode.toString()));
  }
}
