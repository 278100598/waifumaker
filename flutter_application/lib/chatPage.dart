import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:provider/provider.dart';
import 'package:uuid/uuid.dart';
import 'package:open_filex/open_filex.dart';
import 'package:path_provider/path_provider.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'main.dart';

class HttpService {
  final String getURL = "http://54.162.23.86:11234/get";
  final String tokenURL = "http://54.162.23.86:11234/get/with_token";
  final String posttokenURL = "http://54.162.23.86:11234/post/with_token";
  final String headURL = "https://characterai.io/i/80/static/avatars/";
  final String token="579aa6cc6e6096637499c0e89e2e3ab0b2142d25";

  Future<String> getHistorys(String history_id) async {
    var url="https://beta.character.ai/chat/history/msgs/user/?history_external_id=$history_id";
    final http.Response res = await http.get(Uri.parse("$tokenURL?URL=$url&TOKEN=$token"));
    
    if (res.statusCode == 200) {
      return res.body ;
    } else {
      throw "Unable to retrieve posts.";
    }
  }

  Future<String> queryCharacter(String name) async {
    var url="https://beta.character.ai/chat/characters/search/?query=$name";
    final http.Response res = await http.get(Uri.parse("$tokenURL?URL=$url&TOKEN=$token"));

    if (res.statusCode == 200) {
      return res.body ;
    } else {
      throw "Unable to retrieve posts.";
    }
  }

  Future<String> createCharacter(String id) async {
    final url = "https://beta.character.ai/chat/history/create/";
    final data = {"character_external_id":id};
    final header = {"Content-Type": "application/json"};
    final http.Response res = await http.post(Uri.parse("$posttokenURL?URL=$url&TOKEN=$token"),body: jsonEncode(data), headers: header);
    if (res.statusCode == 200) {
      return res.body ;
    } else {
      throw "Unable to retrieve posts.";
    }
  }

  Future<String> continueChat(String id) async {
    final url = "https://beta.character.ai/chat/history/continue/";
    final data = {"character_external_id":id};
    final header = {"Content-Type": "application/json"};
    final http.Response res = await http.post(Uri.parse("$posttokenURL?URL=$url&TOKEN=$token"),body: jsonEncode(data), headers: header);
    if (res.statusCode == 200) {
      return res.body;
    } else {
      throw "Unable to retrieve posts.";
    }
  }

  Future<void> sendMessage(String tgt, String history, String text) async {
    final url = "https://beta.character.ai/chat/streaming/";
    final data = {
      "history_external_id":history,
      "tgt":tgt,
      "text":text,
    };
    final header = {"Content-Type": "application/json"};
    final http.Response res = await http.post(Uri.parse("$posttokenURL?URL=$url&TOKEN=$token"),body: jsonEncode(data), headers: header);
    if (res.statusCode == 200) {
      return;
    } else {
      throw "Unable to retrieve posts.";
    }
  }

}


class ChatPage extends StatefulWidget {
  const ChatPage({super.key});

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  List<types.Message> _messages = [];
  final TextEditingController _searchController = TextEditingController();
  bool _isSearching = false;
  List<dynamic> _filteredData = [];

  final _user = const types.User(
    id: 'xiang1078',
  );

  @override
  void initState() {
    super.initState();
    _searchController.addListener(_performSearch);
    _loadMessages(MyAppState());
  }

  

  void _handleMessageTap(BuildContext _, types.Message message) async {
    if (message is types.FileMessage) {
      var localPath = message.uri;

      if (message.uri.startsWith('http')) {
        try {
          final index =
              _messages.indexWhere((element) => element.id == message.id);
          final updatedMessage =
              (_messages[index] as types.FileMessage).copyWith(
            isLoading: true,
          );

          setState(() {
            _messages[index] = updatedMessage;
          });

          final client = http.Client();
          final request = await client.get(Uri.parse(message.uri));
          final bytes = request.bodyBytes;
          final documentsDir = (await getApplicationDocumentsDirectory()).path;
          localPath = '$documentsDir/${message.name}';

          if (!File(localPath).existsSync()) {
            final file = File(localPath);
            await file.writeAsBytes(bytes);
          }
        } finally {
          final index =
              _messages.indexWhere((element) => element.id == message.id);
          final updatedMessage =
              (_messages[index] as types.FileMessage).copyWith(
            isLoading: null,
          );

          setState(() {
            _messages[index] = updatedMessage;
          });
        }
      }

      await OpenFilex.open(localPath);
    }
  }



  void _handleSendPressed(types.PartialText message, MyAppState appState) async {
    await HttpService().sendMessage(appState.tgt, appState.history_id, message.text);
    _loadMessages(appState);
  }

  void _loadMessages(MyAppState appState) async {
    final response = await HttpService().getHistorys(appState.history_id);
    List<types.Message> messages = [];
    for (var message in (jsonDecode(response)["messages"] as List).reversed) {
      if (!message["src__is_human"]) {
        appState.tgt = message["src__user__username"];
      }
      messages.add(types.Message.fromJson({
        "author": {
          "firstName": message["src__name"],
          "id": message["src__name"],
          "imageUrl": "https://characterai.io/i/80/static/avatars/${message['src__character__avatar_file_name']}",
        },
        "createdAt": DateTime.now().millisecondsSinceEpoch,
        "id": message["uuid"],
        "status": "seen",
        "text": message["text"],
        "type": "text",
      }));
    }
    


    setState(() {
      _messages = messages;
    });
  }

  

  Future<void> _performSearch() async {
    if (_searchController.text == "") {
      setState(() {
        _isSearching = false;
      });
      return;
    }
    

    final characters = jsonDecode(await HttpService().queryCharacter(_searchController.text))["characters"];
    setState(() {
      _isSearching = true;
      _filteredData = characters;
    });
  }

  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();

    return Scaffold(
      appBar: AppBar(
          flexibleSpace: Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.deepPurple, Colors.purple.shade300],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
          ),
          title: TextField(
            controller: _searchController,
            style: const TextStyle(color: Colors.white),
            cursorColor: Colors.white,
            decoration: const InputDecoration(
              hintText: 'Search...',
              hintStyle: TextStyle(color: Colors.white54),
              border: InputBorder.none,
            ),
          ),
        ),
      body: _isSearching ? ListView.builder(
          itemCount: _filteredData.length,
          itemBuilder: (context, index) => ListTile(
            leading: CircleAvatar(
              backgroundImage: CachedNetworkImageProvider("${HttpService().getURL}?URL=${HttpService().headURL}${_filteredData[index]['avatar_file_name']}")
            ),
            title: Text(
              _filteredData[index]["participant__name"],
              style: const TextStyle(color: Colors.blue),
            ),
            onTap: () async {
              var res = await HttpService().continueChat(_filteredData[index]["external_id"]);
              if (res=="there is no history between user and character") {
                res = await HttpService().createCharacter(_filteredData[index]["external_id"]);
              }
              setState(() {
                appState.character_id = _filteredData[index]["external_id"];
                appState.history_id = jsonDecode(res)["external_id"];
                _loadMessages(appState);
                _searchController.clear();
              });
            },
          ),
        ) : Chat(
        messages: _messages,
        onSendPressed:(p0) {
          _handleSendPressed(p0, appState);
        },
        showUserAvatars: true,
        showUserNames: true,
        user: _user,
        theme: const DefaultChatTheme(
          seenIcon: Text(
            'read',
            style: TextStyle(
              fontSize: 10.0,
            ),
          ),
        ),
      ),
    );
  }
  
  
}