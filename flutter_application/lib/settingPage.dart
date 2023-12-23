import 'package:provider/provider.dart';
import 'package:flutter/material.dart';
import 'main.dart';
import 'common.dart';


class SettingPage extends StatefulWidget {
  @override
  State<SettingPage> createState() => _SettingPageState();
}

class _SettingPageState extends State<SettingPage> with WidgetsBindingObserver {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _textController1 = TextEditingController();
  final TextEditingController _textController2 = TextEditingController();

  @override
  void dispose() {
    ambiguate(WidgetsBinding.instance)!.removeObserver(this);
    // Release decoders and buffers back to the operating system making them
    // available for other apps to use.
    _textController1.dispose();
    _textController2.dispose();
    super.dispose();
  }


  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();
    _textController1.text = appState.chat_token;
    _textController2.text = appState.pixiv_cookie;

    return Scaffold(
      appBar: AppBar(title: Text("Setting")),
      body: Padding(
        padding: const EdgeInsets.all(25),
        child: Form(
          key: _formKey,
          autovalidateMode: AutovalidateMode.onUserInteraction,
          child: ListView(
            padding: EdgeInsets.all(4),
            children: <Widget>[
              Text("character.ai Token"),
              Divider(),
              SizedBox(
                width: 250,
                child: TextField(
                  controller: _textController1,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'Token',
                  ),
                  onChanged: (text) {
                    appState.chat_token = text;
                  },
                ),
              ),
              Padding(padding: EdgeInsets.all(8)),
              Text("Pixiv Cookie"),
              Divider(),
              SizedBox(
                width: 250,
                child: TextField(
                  controller: _textController2,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'Cookie',
                  ),
                  onChanged: (text) {
                    appState.pixiv_cookie = text;
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }



  
}





