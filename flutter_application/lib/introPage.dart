
import 'package:flutter/material.dart';

class IntroPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final white = Colors.white, black = Colors.black;

    return ListView(
      children: [
        Center(
          child: Card(
            color: white,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text (
                "Welcome",
                style: theme.textTheme.displayMedium!.copyWith(color: black),
              ),
            ),
          ),
        ),
        Center(
          child: Card(
            color: white,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: SelectableText (
                "If you want to try Stable Diffusion\n"
                "you can visit this url\n"
                "https://stable-diffusion-ui.le37.tw/\n"
                "or you can try this website\n"
                "https://civitai.com/"
                , 
                style: theme.textTheme.bodyMedium!.copyWith(color: black),
                textAlign: TextAlign.center,
              ),
            ),
          ),
        ),
        Center(
          child: Card(
            color: white,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  SelectableText (
                    "Scraper"
                    ,
                    style: theme.textTheme.headlineMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                  SelectableText (
                    "you can use search bar to search character\n"
                    "and then click on the character\n"
                    "aws lambda will scrap images of the character"
                    , 
                    style: theme.textTheme.bodyMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
        ),
        Center(
          child: Card(
            color: white,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  SelectableText (
                    "Gallery"
                    ,
                    style: theme.textTheme.headlineMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                  SelectableText (
                    "what you search in the Scraper page can be find here"
                    , 
                    style: theme.textTheme.bodyMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
        ),
        Center(
          child: Card(
            color: white,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  SelectableText (
                    "Chat"
                    ,
                    style: theme.textTheme.headlineMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                  SelectableText (
                    "you can chat with character of character.ai here"
                    , 
                    style: theme.textTheme.bodyMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
        ),
        Center(
          child: Card(
            color: white,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  SelectableText (
                    "Voice"
                    ,
                    style: theme.textTheme.headlineMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                  SelectableText (
                    "you can generate character's talking audio with any text\n"
                    "the original website is this\n"
                    "https://genshinvoice.top/"
                    , 
                    style: theme.textTheme.bodyMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
        ),
        Center(
          child: Card(
            color: white,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  SelectableText (
                    "Generate Word"
                    ,
                    style: theme.textTheme.headlineMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                  SelectableText (
                    "Flutter's example app\n"
                    "can generate random word pair"
                    , 
                    style: theme.textTheme.bodyMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
        ),
        Center(
          child: Card(
            color: white,
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  SelectableText (
                    "Generate History"
                    ,
                    style: theme.textTheme.headlineMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                  SelectableText (
                    "Flutter's example app\n"
                    "can list random words you like"
                    , 
                    style: theme.textTheme.bodyMedium!.copyWith(color: black),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }
}