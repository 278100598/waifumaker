import 'package:flutter/material.dart';
import 'package:xml/xml.dart';
import 'package:http/http.dart' as http;
import 'constant.dart' as Constant;

class HttpService {
  final String getURL = "http://${Constant.BASE_IP}:11234/get";
  final String sqsURL = "http://${Constant.BASE_IP}:11234/get/sqs";

  Future<String> searchTag(String tag) async {
    final http.Response res = await http.get(Uri.parse("$getURL?URL=https://yande.re/tag.xml?order=count%26name=$tag"));
    
    if (res.statusCode == 200) {
      return res.body ;
    } else {
      throw "Unable to retrieve posts.";
    }
  }

  Future<void> sendSQS(String tag) async {
    final http.Response res = await http.get(Uri.parse("$sqsURL?TAG=$tag"));
    if (res.statusCode != 200) {
      throw "sendSQS res.statusCode != 200";
    }
  }

}



class SQSPage extends StatefulWidget {
  @override
  State<SQSPage> createState() => _SQSPageState();
}

class _SQSPageState extends State<SQSPage> {
  String searchValue = '';

  

  final TextEditingController _searchController = TextEditingController();
  final List<String> _data = [];
  List<String> _filteredData = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _filteredData = _data;
    _searchController.addListener(_performSearch);
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _performSearch() async {
    setState(() {
      _isLoading = true;
    });

    //Simulates waiting for an API call
    var res = await HttpService().searchTag(_searchController.text);
    var document = XmlDocument.parse(res).findAllElements("tag");
    setState(() {
      _filteredData = document.map(
        (e) => "${e.getAttribute('name')} (${e.getAttribute('count')})"
      ).toList();
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) => Scaffold(
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
    body: _isLoading
        ? const Center(
            child: CircularProgressIndicator(color: Colors.white),
          )
        : ListView.builder(
            itemCount: _filteredData.length,
            itemBuilder: (context, index) => ListTile(
              onTap: () async {
                final tag = _filteredData[index].substring(0,_filteredData[index].lastIndexOf(" "));
                await HttpService().sendSQS(tag);
              },
              title: Text(
                _filteredData[index],
                style: const TextStyle(color: Colors.white),
              ),
            ),
          ),
    backgroundColor: Colors.deepPurple.shade900,
  );
}