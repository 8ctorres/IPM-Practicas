// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'imgresponse.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ResponseModel _$ImgResponseFromJson(Map<String, dynamic> json) {
  return ResponseModel(
    json['result'] == null
        ? null
        : Result.fromJson(json['result'] as Map<String, dynamic>),
    json['status'] == null
        ? null
        : Status.fromJson(json['status'] as Map<String, dynamic>),
  );
}

Map<String, dynamic> _$ImgResponseToJson(ResponseModel instance) =>
    <String, dynamic>{
      'result': instance.result?.toJson(),
      'status': instance.status?.toJson(),
    };

Result _$ResultFromJson(Map<String, dynamic> json) {
  return Result(
    (json['tags'] as List)
        ?.map((e) =>
            e == null ? null : TagItem.fromJson(e as Map<String, dynamic>))
        ?.toList(),
  );
}

Map<String, dynamic> _$ResultToJson(Result instance) => <String, dynamic>{
      'tags': instance.tags,
    };

Status _$StatusFromJson(Map<String, dynamic> json) {
  return Status(
    json['text'] as String,
    json['type'] as String,
  );
}

Map<String, dynamic> _$StatusToJson(Status instance) => <String, dynamic>{
      'text': instance.text,
      'type': instance.type,
    };

TagItem _$TagItemFromJson(Map<String, dynamic> json) {
  return TagItem(
    (json['confidence'] as num)?.toDouble(),
    json['tag'] == null
        ? null
        : Tag.fromJson(json['tag'] as Map<String, dynamic>),
  );
}

Map<String, dynamic> _$TagItemToJson(TagItem instance) => <String, dynamic>{
      'confidence': instance.confidence,
      'tag': instance.tag,
    };

Tag _$TagFromJson(Map<String, dynamic> json) {
  return Tag(
    json['en'] as String,
    json['es'] as String,
  );
}

Map<String, dynamic> _$TagToJson(Tag instance) => <String, dynamic>{
      'en': instance.en,
      'es': instance.es,
    };
