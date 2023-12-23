import 'package:english_words/english_words.dart';
import 'package:flutter/material.dart';
import 'package:namer_app/introPage.dart';
import 'package:provider/provider.dart';
import 'chatPage.dart';
import 'imagePage.dart';
import 'sqsPage.dart';
import 'voicePage.dart';
import 'pixivPage.dart';
import 'settingPage.dart';
import 'constant.dart' as Constant;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => MyAppState(),
      child: MaterialApp(
        title: 'Waifu Maker',
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.lightBlue),
        ),
        home: MyHomePage(),
      ),
    );
  }
}

class MyAppState extends ChangeNotifier {
  var current = WordPair.random();
  var voice_character = "符玄_ZH";
  var voice_lang = "ZH";
  var voice_text = "相對論是關於時空和重力的理論，主要由愛因斯坦創立，依其研究對象的不同可分為狹義相對論和廣義相對論。";
  var voice_url = "http://${Constant.BASE_IP}:11234/get?URL=https://waifumakerbucket2.s3.amazonaws.com/Voice/%E7%AC%A6%E7%8E%84_ZH_ZH_%E7%9B%B8%E5%B0%8D%E8%AB%96%E6%98%AF%E9%97%9C%E6%96%BC%E6%99%82%E7%A9%BA%E5%92%8C%E9%87%8D%E5%8A%9B%E7%9A%84%E7%90%86%E8%AB%96%EF%BC%8C%E4%B8%BB%E8%A6%81%E7%94%B1%E6%84%9B%E5%9B%A0%E6%96%AF%E5%9D%A6%E5%89%B5%E7%AB%8B%EF%BC%8C%E4%BE%9D%E5%85%B6%E7%A0%94%E7%A9%B6%E5%B0%8D%E8%B1%A1%E7%9A%84%E4%B8%8D%E5%90%8C%E5%8F%AF%E5%88%86%E7%82%BA%E7%8B%B9%E7%BE%A9%E7%9B%B8%E5%B0%8D%E8%AB%96%E5%92%8C%E5%BB%A3%E7%BE%A9%E7%9B%B8%E5%B0%8D%E8%AB%96%E3%80%82.wav";
  var voice_time = Duration.zero;
  var pixiv_mode = "safe";
  var pixiv_ai = "Yes";
  var pixiv_keyword = "";
  var pixiv_cookie = "first_visit_datetime_pc=2023-12-06%2002%3A30%3A04; yuid_b=I1NGCUA; p_ab_id=7; p_ab_id_2=2; p_ab_d_id=1213741604; PHPSESSID=35673257_oZsuLoF9gGbrzhcbhIMauGAPVO5KWLUs; device_token=51387302cc6ac444401fd5bdef37363e; _ga_MZ1NL4PHH0=GS1.1.1701797514.1.1.1701797526.0.0.0; c_type=32; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; cf_clearance=qq.P0AJR37AVvyZwStlMmXuapzLcw1PlZGq0g9sUAyE-1703248618-0-2-c09965ff.36ccb9e3.d8889a89-0.2.1703248618; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; _gid=GA1.2.372031141.1703248627; __cf_bm=6rG_kJ3AqLe8yEYNvUpQdSidjBvUvOCeMes2AoZrJtA-1703250749-1-AS1ToRVIMXCAcD42PRVZZXsEqQIcmmmrRd70JyCC09h3j2lFytivpoH5XwILXKJ3+r/zyFaXZYvM6MscmCYNdZhU/dSQHwCHIBT9p+g53dzB; _ga=GA1.1.387688919.1701797405; _ga_75BBYNYN9J=GS1.1.1703248617.2.1.1703251821.0.0.0";
  String character_id = "IVnSUJD1hgZYDii01envVlZa21hJfx77VULPvYx8XJo";
  String history_id = "F_aU9WkY9SGgN77ch9tgxoQylU9yAiKRNWdEyRE4Eoo";
  String tgt = "internal_id:40606:65905abc-64e2-4a9d-b96d-8da3142b91c7";
  var chat_token = "579aa6cc6e6096637499c0e89e2e3ab0b2142d25";

  void getNext() {
    current = WordPair.random();
    notifyListeners();
  }

  var favorites = <WordPair>{};
  


  void toggleFavorite() {
    if (favorites.contains(current)) {
      favorites.remove(current);
    } else {
      favorites.add(current);
    }
    notifyListeners();
  }
}

class MyHomePage extends StatefulWidget {
  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var selectedIndex = 0; 

  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();
    
    Widget page;
    switch (selectedIndex) {
      case 0:
        page = IntroPage();
      case 1:
        page = PixivPage();
      case 2:
        page = SQSPage();
      case 3:
        page = ImagePage();
      case 4:
        page = ChatPage(appState);
      case 5:
        page = VoicePage();
      case 6:
        page = GeneratorPage();
      case 7:
        page = FPage();
      case 8:
        page = SettingPage();
      default:
        throw UnimplementedError('no widget for $selectedIndex');
    }

    return LayoutBuilder(
      builder: (context, constraints) {
        return Scaffold(
          body: Row(
            children: [
              SafeArea(
                child: NavigationRail(
                  extended: constraints.maxWidth >= 600,
                  destinations: [
                    NavigationRailDestination(
                      icon: Icon(Icons.home),
                      label: Text('Home'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.brush),
                      label: Text('PixivScraper'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.zoom_in),
                      label: Text('Scraper'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.image),
                      label: Text('Gallery'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.chat),
                      label: Text('Chat'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.keyboard_voice),
                      label: Text('Voice'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.abc),
                      label: Text('Generate Word'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.history),
                      label: Text('Generate History'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.settings),
                      label: Text('Setting'),
                    ),
                  ],
                  selectedIndex: selectedIndex,
                  onDestinationSelected: (value) {
                    setState(() {
                      selectedIndex = value;
                    });
                  },
                ),
              ),
              Expanded(
                child: Container(
                  color: Theme.of(context).colorScheme.primaryContainer,
                  child: page,
                ),
              ),
            ],
          ),
        );
      }
    );
  }
}


class FPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();

    if (appState.favorites.isEmpty) {
      return Center(
        child: Text('No favorites yet.'),
      );
    }

    return ListView(
      children: [
        Padding(
          padding: const EdgeInsets.all(20),
          child: Text('You have '
              '${appState.favorites.length} favorites:'),
        ),
        for (var pair in appState.favorites)
          ListTile(
            leading: Icon(Icons.favorite),
            title: Text(pair.asLowerCase),
          ),
      ],
    );
  }
}

class GeneratorPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();
    var pair = appState.current;

    IconData icon;
    if (appState.favorites.contains(pair)) {
      icon = Icons.favorite;
    } else {
      icon = Icons.favorite_border;
    }
    

    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          BigCard(pair: pair),
          SizedBox(height: 10),
          Row(
            mainAxisSize: MainAxisSize.min, 
            children: [
              ElevatedButton.icon(
                onPressed: () {
                  appState.toggleFavorite();
                },
                icon: Icon(icon),
                label: Text('Like'),
              ),
              ElevatedButton(
                onPressed: () {
                  appState.getNext();
                },
                child: Text('Next'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class BigCard extends StatelessWidget {
  const BigCard({
    super.key,
    required this.pair,
  });

  final WordPair pair;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final style = theme.textTheme.displayMedium!.copyWith(
      color: theme.colorScheme.onPrimary,
    );

    return Card(
      color: theme.colorScheme.primary,
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Text(
          pair.asLowerCase, 
          style: style,
          semanticsLabel: "${pair.first} ${pair.second}",
        ),
      ),
    );
  }
}