import 'dart:html';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:easy_web_view/easy_web_view.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.red,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String lastMessage = '';

  void handleMessage(Event event) async {
    MessageEvent messageEvent = event as MessageEvent;
    lastMessage = messageEvent.data.toString();
    debugPrint("flutter got $lastMessage");
  }

  @override
  void initState() {
    window.addEventListener("message", handleMessage);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
          return EasyWebView(
            key: UniqueKey(),
            height: constraints.maxHeight,
            width: constraints.maxWidth,
            src:
                '${kDebugMode ? 'http://localhost:8000' : Uri.base.origin}/v1/graph',
          );
        },
      ),
    );
  }
}
