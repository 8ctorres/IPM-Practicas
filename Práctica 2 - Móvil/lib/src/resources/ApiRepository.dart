import 'dart:io';
import 'package:iagram/src/models/imgresponse.dart';

import 'ApiProvider.dart';

class ApiRepository {
  final _provider = ApiProvider();

  Future<ResponseModel> getTags(File image){
    return _provider.getTags(image);
  }
}

class NetworkError extends Error{}
