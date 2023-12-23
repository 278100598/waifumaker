import 'package:provider/provider.dart';
import 'package:flutter/material.dart';
import 'dart:convert';
import 'main.dart';
import 'package:http/http.dart' as http;
import 'package:dropdown_search/dropdown_search.dart';
import 'common.dart';
import 'constant.dart' as Constant;

class HttpService {
  final String getURL = "http://${Constant.BASE_IP}:11234/get";
  final String pixivURL = "http://${Constant.BASE_IP}:11234/post/pixiv";

  Future<void> searchKeyword(String keyword, String mode, String ai, String cookie) async {
    final data = {
      "cookie": cookie,
      "keyword": keyword,
      "ai": ai,
      "mode": mode,
    };
    final header = {"Content-Type": "application/json"};
    final http.Response res = await http.post(Uri.parse(pixivURL) ,body: jsonEncode(data), headers: header);
    
    if (res.statusCode != 200) {
      throw "searchKeyword res.statusCode != 200";
    }
  }
}

class PixivPage extends StatefulWidget {
  @override
  State<PixivPage> createState() => _PixivPageState();
}

class _PixivPageState extends State<PixivPage> with WidgetsBindingObserver {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _textController = TextEditingController();


  @override
  void dispose() {
    ambiguate(WidgetsBinding.instance)!.removeObserver(this);
    // Release decoders and buffers back to the operating system making them
    // available for other apps to use.
    _textController.dispose();
    super.dispose();
  }


  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();
    _textController.text = appState.pixiv_keyword;

    return Scaffold(
      appBar: AppBar(title: Text("Pixiv Keyword Scraper")),
      body: Padding(
        padding: const EdgeInsets.all(25),
        child: Form(
          key: _formKey,
          autovalidateMode: AutovalidateMode.onUserInteraction,
          child: ListView(
            padding: EdgeInsets.all(4),
            children: <Widget>[
              Text("使用模式"),
              Divider(),
              Row(
                children: [
                  Expanded(
                    child: DropdownSearch<String>(
                      selectedItem: appState.pixiv_mode,
                      items: ["safe","r18"],
                      dropdownDecoratorProps: DropDownDecoratorProps(
                        dropdownSearchDecoration: InputDecoration(
                          labelText: 'mode *',
                          filled: true,
                          fillColor: Theme.of(context).inputDecorationTheme.fillColor,
                        ),
                      ),
                      onChanged: (value) {
                        appState.pixiv_mode = value ?? "";
                      },
                    ),
                  ),
                ],
              ),
              Padding(padding: EdgeInsets.all(8)),
              Text("是否包含ai生成圖片"),
              Divider(),
              Row(
                children: [
                  Expanded(
                    child: DropdownSearch<String>(
                      selectedItem: appState.pixiv_ai,
                      items: ["Yes","No"],
                      dropdownDecoratorProps: DropDownDecoratorProps(
                        dropdownSearchDecoration: InputDecoration(
                          labelText: 'ai *',
                          filled: true,
                          fillColor: Theme.of(context).inputDecorationTheme.fillColor,
                        ),
                      ),
                      onChanged: (value) {
                        appState.pixiv_ai = value ?? "";
                      },
                    ),
                  ),
                ],
              ),
              Padding(padding: EdgeInsets.all(8)),
              Text("關鍵字"),
              Divider(),
              SizedBox(
                width: 250,
                child: TextField(
                  controller: _textController,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'Keyword',
                  ),
                  onChanged: (text) {
                    appState.pixiv_keyword = text;
                  },
                ),
              ),
              Padding(padding: EdgeInsets.all(8)),
              ElevatedButton.icon(
                onPressed: () async {
                  if (appState.pixiv_mode != "" && appState.pixiv_ai != "" && _textController.text != "") {
                    await HttpService().searchKeyword(_textController.text, appState.pixiv_mode, appState.pixiv_ai, appState.pixiv_cookie);
                  }
                },
                icon: Icon(Icons.image_search),
                label: Text('Search!'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  
}





