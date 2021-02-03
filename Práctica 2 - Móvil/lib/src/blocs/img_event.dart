part of 'img_bloc.dart';

abstract class ImgEvent extends Equatable {
  const ImgEvent();
}

class GetTags extends ImgEvent {
  final File _image;

  GetTags(this._image);
  @override
  List<Object> get props => [_image];
}
