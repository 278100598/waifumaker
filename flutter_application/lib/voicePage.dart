import 'package:provider/provider.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:convert';
import 'main.dart';
import 'package:http/http.dart' as http;
import 'package:dropdown_search/dropdown_search.dart';
import 'package:just_audio/just_audio.dart';
import 'package:rxdart/rxdart.dart';
import 'package:audio_session/audio_session.dart';
import 'common.dart';
import 'constant.dart' as Constant;

class HttpService {
  final String getURL = "http://${Constant.BASE_IP}:11234/get";
  final String postvoiceURL = "http://${Constant.BASE_IP}:11234/post/vocie";
  final String getlistURL = "http://${Constant.BASE_IP}:11234/get/voice_list";

  Future<String> generateVoice(String speaker, String lang, String text) async {
    var url="$postvoiceURL";
    final header = {"Content-Type": "application/json"};
    var data = {
      "BUCKET": "waifumakerbucket1",
      "SPEAKER": speaker,
      "LANG": lang,
      "TEXT": text,
    };
    final http.Response res = await http.post(Uri.parse(postvoiceURL), body: jsonEncode(data), headers: header);
    
    if (res.statusCode == 200) {
      return res.body;
    } else {
      throw "Unable to retrieve posts.";
    }
  }

  Future<String> getList() async {
    final http.Response res = await http.get(Uri.parse(getlistURL));
    
    if (res.statusCode == 200) {
      return res.body;
    } else {
      throw "Unable to retrieve posts.";
    }
  }

}

class VoicePage extends StatefulWidget {
  @override
  State<VoicePage> createState() => _VoicePageState();
}

class _VoicePageState extends State<VoicePage> with WidgetsBindingObserver {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _textController = TextEditingController();

  final _player = AudioPlayer();

  @override
  void initState() {
    super.initState();
    ambiguate(WidgetsBinding.instance)!.addObserver(this);
    SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
      statusBarColor: Colors.black,
    ));
    _textController.text = "相對論是關於時空和重力的理論，主要由愛因斯坦創立，依其研究對象的不同可分為狹義相對論和廣義相對論。";
    _init();
  }

  Future<void> _init() async {
    // Inform the operating system of our app's audio attributes etc.
    // We pick a reasonable default for an app that plays speech.
    final session = await AudioSession.instance;
    await session.configure(const AudioSessionConfiguration.speech());
    // Listen to errors during playback.
    _player.playbackEventStream.listen((event) {},
        onError: (Object e, StackTrace stackTrace) {
      print('A stream error occurred: $e');
    });
    // Try to load audio from a source and catch any errors.
    try {
      // AAC example: https://dl.espressif.com/dl/audio/ff-16b-2c-44100hz.aac
      await _player.setAudioSource(AudioSource.uri(Uri.parse(
          "https://waifumakerbucket1.s3.amazonaws.com/Voice/%E7%AC%A6%E7%8E%84_ZH_ZH_%E7%9B%B8%E5%B0%8D%E8%AB%96%E6%98%AF%E9%97%9C%E6%96%BC%E6%99%82%E7%A9%BA%E5%92%8C%E9%87%8D%E5%8A%9B%E7%9A%84%E7%90%86%E8%AB%96%EF%BC%8C%E4%B8%BB%E8%A6%81%E7%94%B1%E6%84%9B%E5%9B%A0%E6%96%AF%E5%9D%A6%E5%89%B5%E7%AB%8B%EF%BC%8C%E4%BE%9D%E5%85%B6%E7%A0%94%E7%A9%B6%E5%B0%8D%E8%B1%A1%E7%9A%84%E4%B8%8D%E5%90%8C%E5%8F%AF%E5%88%86%E7%82%BA%E7%8B%B9%E7%BE%A9%E7%9B%B8%E5%B0%8D%E8%AB%96%E5%92%8C%E5%BB%A3%E7%BE%A9%E7%9B%B8%E5%B0%8D%E8%AB%96%E3%80%82.wav"
      )));
    } catch (e) {
      print("Error loading audio source: $e");
    }
  }

  @override
  void dispose() {
    ambiguate(WidgetsBinding.instance)!.removeObserver(this);
    // Release decoders and buffers back to the operating system making them
    // available for other apps to use.
    _player.dispose();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused) {
      // Release the player's resources when not in use. We use "stop" so that
      // if the app resumes later, it will still remember what position to
      // resume from.
      _player.stop();
    }
  }

  Stream<PositionData> get _positionDataStream =>
      Rx.combineLatest3<Duration, Duration, Duration?, PositionData>(
          _player.positionStream,
          _player.bufferedPositionStream,
          _player.durationStream,
          (position, bufferedPosition, duration) => PositionData(
              position, bufferedPosition, duration ?? Duration.zero));

  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();
    appState.voice_text = _textController.text;


    return Scaffold(
      appBar: AppBar(title: Text("Voice Generating")),
      body: Padding(
        padding: const EdgeInsets.all(25),
        child: Form(
          key: _formKey,
          autovalidateMode: AutovalidateMode.onUserInteraction,
          child: ListView(
            padding: EdgeInsets.all(4),
            children: <Widget>[
              Text("角色_配音"),
              Divider(),
              Row(
                children: [
                  Expanded(
                    child: DropdownSearch<String>(
                      selectedItem: appState.voice_character,
                      asyncItems: (String? filter) => getData(filter),
                      popupProps: PopupPropsMultiSelection.modalBottomSheet(
                        showSelectedItems: true,
                        itemBuilder: _customPopupItemBuilderExample2,
                        showSearchBox: true,
                      ),
                      compareFn: (item, sItem) => item == sItem,
                      dropdownDecoratorProps: DropDownDecoratorProps(
                        dropdownSearchDecoration: InputDecoration(
                          labelText: 'User *',
                          filled: true,
                          fillColor: Theme.of(context).inputDecorationTheme.fillColor,
                        ),
                      ),
                      onChanged: (value) {
                        appState.voice_character = value ?? "";
                      },
                    ),
                  ),
                ],
              ),
              Padding(padding: EdgeInsets.all(8)),
              Text("使用語言"),
              Divider(),
              Row(
                children: [
                  Expanded(
                    child: DropdownSearch<String>(
                      selectedItem: appState.voice_lang,
                      items: ["ZH","EN","JP"],
                      dropdownDecoratorProps: DropDownDecoratorProps(
                        dropdownSearchDecoration: InputDecoration(
                          labelText: 'Language *',
                          filled: true,
                          fillColor: Theme.of(context).inputDecorationTheme.fillColor,
                        ),
                      ),
                      onChanged: (value) {
                        appState.voice_lang = value ?? "";
                      },
                    ),
                  ),
                ],
              ),
              Padding(padding: EdgeInsets.all(8)),
              Text("文字"),
              Divider(),
              SizedBox(
                width: 250,
                child: TextField(
                  controller: _textController,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'Text',
                  ),
                ),
              ),
              Padding(padding: EdgeInsets.all(8)),
              ElevatedButton.icon(
                onPressed: () async {
                  if (appState.voice_character != "" && appState.voice_lang != "" && _textController.text != "") {
                    final result = await HttpService().generateVoice(appState.voice_character, appState.voice_lang, _textController.text);
                    await _player.setAudioSource(
                      AudioSource.uri(
                        Uri.parse(result)
                      )
                    );
                  }
                },
                icon: Icon(Icons.voice_chat),
                label: Text('Generate!'),
              ),
              Padding(padding: EdgeInsets.all(20)),
              Center(
                child: ControlButtons(_player)
              ),
              // Display seek bar. Using StreamBuilder, this widget rebuilds
              // each time the position, buffered position or duration changes.
              StreamBuilder<PositionData>(
                stream: _positionDataStream,
                builder: (context, snapshot) {
                  final positionData = snapshot.data;
                  return SeekBar(
                    duration: positionData?.duration ?? Duration.zero,
                    position: positionData?.position ?? Duration.zero,
                    bufferedPosition:
                        positionData?.bufferedPosition ?? Duration.zero,
                    onChangeEnd: _player.seek,
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }


  Widget _customPopupItemBuilderExample2(BuildContext context, String item, bool isSelected) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 8),
      decoration: !isSelected
          ? null
          : BoxDecoration(
              border: Border.all(color: Theme.of(context).primaryColor),
              borderRadius: BorderRadius.circular(5),
              color: Colors.white,
            ),
      child: ListTile(
        selected: isSelected,
        title: Text(item)
      ),
    );
  }

  Future<List<String>> getData(filter) async {
    final _loadedData = await HttpService().getList();
    
    return [
      for (String char in jsonDecode(_loadedData))
        char
    ];
  }

  
}




class ControlButtons extends StatelessWidget {
  final AudioPlayer player;

  const ControlButtons(this.player, {Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Opens volume slider dialog
        IconButton(
          icon: const Icon(Icons.volume_up),
          onPressed: () {
            showSliderDialog(
              context: context,
              title: "Adjust volume",
              divisions: 10,
              min: 0.0,
              max: 1.0,
              value: player.volume,
              stream: player.volumeStream,
              onChanged: player.setVolume,
            );
          },
        ),

        /// This StreamBuilder rebuilds whenever the player state changes, which
        /// includes the playing/paused state and also the
        /// loading/buffering/ready state. Depending on the state we show the
        /// appropriate button or loading indicator.
        StreamBuilder<PlayerState>(
          stream: player.playerStateStream,
          builder: (context, snapshot) {
            final playerState = snapshot.data;
            final processingState = playerState?.processingState;
            final playing = playerState?.playing;
            if (processingState == ProcessingState.loading ||
                processingState == ProcessingState.buffering) {
              return Container(
                margin: const EdgeInsets.all(8.0),
                width: 64.0,
                height: 64.0,
                child: const CircularProgressIndicator(),
              );
            } else if (playing != true) {
              return IconButton(
                icon: const Icon(Icons.play_arrow),
                iconSize: 64.0,
                onPressed: player.play,
              );
            } else if (processingState != ProcessingState.completed) {
              return IconButton(
                icon: const Icon(Icons.pause),
                iconSize: 64.0,
                onPressed: player.pause,
              );
            } else {
              return IconButton(
                icon: const Icon(Icons.replay),
                iconSize: 64.0,
                onPressed: () {
                  player.pause();
                  player.seek(Duration.zero);
                },
              );
            }
          },
        ),
        // Opens speed slider dialog
        StreamBuilder<double>(
          stream: player.speedStream,
          builder: (context, snapshot) => IconButton(
            icon: Text("${snapshot.data?.toStringAsFixed(1)}x",
                style: const TextStyle(fontWeight: FontWeight.bold)),
            onPressed: () {
              showSliderDialog(
                context: context,
                title: "Adjust speed",
                divisions: 10,
                min: 0.5,
                max: 1.5,
                value: player.speed,
                stream: player.speedStream,
                onChanged: player.setSpeed,
              );
            },
          ),
        ),
      ],
    );
  }
}

