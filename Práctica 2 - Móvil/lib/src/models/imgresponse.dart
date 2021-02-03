import 'package:json_annotation/json_annotation.dart';
part 'imgresponse.g.dart';

@JsonSerializable(explicitToJson: true)
class ResponseModel {
  ResponseModel(this.result, this.status);
  Result result;
  Status status;

  //Result get result => _result;
  //Status get status => _status;

  factory ResponseModel.fromJson(Map<String, dynamic> json) =>
      _$ImgResponseFromJson(json);

  Map<String, dynamic> toJson() => _$ImgResponseToJson(this);
}

@JsonSerializable()
class Result {
  Result(this.tags);
  List<TagItem> tags;

  //List<TagItem> get tags => _tags;

  factory Result.fromJson(Map<String, dynamic> json) => _$ResultFromJson(json);

  Map<String, dynamic> toJson() => _$ResultToJson(this);
}

@JsonSerializable()
class Status {
  Status(this.text, this.type);
  String text;
  String type;

  //String get text => _text;
  //String get type => _type;

  factory Status.fromJson(Map<String, dynamic> json) => _$StatusFromJson(json);

  Map<String, dynamic> toJson() => _$StatusToJson(this);
}

@JsonSerializable()
class TagItem {
  TagItem(this.confidence, this.tag);
  double confidence;
  Tag tag;

  //double get confidence => _confidence;
  //Tag get tag => _tag;

  factory TagItem.fromJson(Map<String, dynamic> json) =>
      _$TagItemFromJson(json);

  Map<String, dynamic> toJson() => _$TagItemToJson(this);
}

@JsonSerializable()
class Tag {
  Tag(this.en, this.es);
  String en;
  String es;

  //String get en => _en;
  //String get es => _es;

  factory Tag.fromJson(Map<String, dynamic> json) => _$TagFromJson(json);

  Map<String, dynamic> toJson() => _$TagToJson(this);
}
