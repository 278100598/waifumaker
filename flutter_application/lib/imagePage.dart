import 'dart:convert';
import 'package:photo_view/photo_view_gallery.dart';
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:http/http.dart' as http;

class HttpService {
  final String gets3listURL = "http://54.162.23.86:11234/get/s3_list";

  Future<String> listObject(String path) async {
    final http.Response res = await http.get(Uri.parse("$gets3listURL?BUCKET=waifumakerbucket&PREFIX=$path"));
    
    if (res.statusCode == 200) {
      return res.body ;
    } else {
      throw "Unable to retrieve posts.";
    }
  }

}

class ImagePage extends StatefulWidget {

  @override
  State<ImagePage> createState() => _ImagePageState();
}

class _ImagePageState extends State<ImagePage> {
  List<String> path = ["yandere/"];
  
  @override
  Widget build(BuildContext context) {
    

    var prefix_path = "";
    for (String p in path) {
      prefix_path += p;
    }
    final s3_url = "https://waifumakerbucket.s3.amazonaws.com/";
    final appbar = AppBar(
      leading: IconButton(
        icon: Icon(Icons.arrow_back, color: Colors.black),
        onPressed: () {
          if (path.length > 1) {
            setState(() {
              path.removeLast();
            });
          }
        },
      ), 
      title: Text("Gallery"),
      centerTitle: true,
    );
    

    return FutureBuilder(
      future: HttpService().listObject(prefix_path),
      builder: (BuildContext context, AsyncSnapshot<String> snapshot) {
        if (snapshot.hasData) {
          List<dynamic> objects = jsonDecode(snapshot.data!);
          if (objects[0].toString().contains(".jpg")) {
            List<String> images = [], original_images = [];
            for (var object in objects) {
              if(object.toString().contains("preview")) {
                images.add("http://54.162.23.86:11234/get?URL=$s3_url${object.toString()}");
              } else {
                original_images.add("http://54.162.23.86:11234/get?URL=$s3_url${object.toString()}");
              }
            }

            return Scaffold(
              appBar: appbar,
              // Body area
              body: SafeArea(
                  child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: <Widget>[
                  Expanded(
                      child: Container(
                          padding:
                              const EdgeInsets.symmetric(horizontal: 10, vertical: 20),
                          decoration: const BoxDecoration(
                            color: Colors.white,
                          ),
                          child: GridView.builder(
                            gridDelegate:
                                const SliverGridDelegateWithFixedCrossAxisCount(
                              crossAxisCount: 3,
                              crossAxisSpacing: 5,
                              mainAxisSpacing: 5,
                            ),
                            itemBuilder: (context, index) {
                              return RawMaterialButton(
                                child: InkWell(
                                  child: Ink.image(
                                    image: CachedNetworkImageProvider(images[index]),
                                    height: 300,
                                    fit: BoxFit.cover,
                                  ),
                                ),
                                onPressed: () {
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (context) => GalleryWidget(
                                        urlImages: original_images,
                                        index: index,
                                      )
                                    )
                                  );
                                },
                              );
                            },
                            itemCount: images.length,
                        )
                      )
                    )
                  ],
                )
              ),
            );
          } else {
            return Scaffold(
              appBar: appbar,
              body: Padding(
                padding: const EdgeInsets.all(8.0),
                child: ListView(
                  children: [
                    for (var object in objects)
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: ElevatedButton.icon(
                          onPressed: () {
                            setState(() {
                              path.add(object.toString().replaceAll(prefix_path, ""));
                            });
                          },
                          icon: Icon(Icons.image),
                          label: Text(object),
                        ),
                      ),
                  ],
                ),
              ),
            );
          }
        } else {
          return Center(child: CircularProgressIndicator());
        }
      }
    );
  }
}



class GalleryWidget extends StatefulWidget {

  final List<String> urlImages;
  final int index;
  final PageController pageController;
  // ignore: use_key_in_widget_constructors
  GalleryWidget({
    required this.urlImages,
    this.index = 0,
  }) : pageController = PageController(initialPage: index);
  @override
  State<GalleryWidget> createState() => _GalleryWidgetState();
}
class _GalleryWidgetState extends State<GalleryWidget> {
  var urlImage;
  @override
  void initState() {
    super.initState();
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.white,
        centerTitle: true,
        title: const Text(
          'Gallery',
          style: TextStyle(color: Colors.black),
        ),
        iconTheme: const IconThemeData(color: Colors.black),
        leading: IconButton(
            onPressed: () => Navigator.of(context).pop(),
            icon: const Icon(Icons.arrow_back)),
      ),
      body: Column(
        children: <Widget>[
          Expanded(
            child: PhotoViewGallery.builder(
              pageController: widget.pageController,
              itemCount: widget.urlImages.length,
              builder: (context, index) {
                urlImage = widget.urlImages[index];
                return PhotoViewGalleryPageOptions(
                  imageProvider: CachedNetworkImageProvider(urlImage),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}