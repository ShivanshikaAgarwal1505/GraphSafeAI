import 'package:flutter/material.dart';

import '../screens/home/home_screen.dart';

class GraphSafeAIApp extends StatelessWidget {
  const GraphSafeAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GraphSafeAI',
      debugShowCheckedModeBanner: false,
      home: const HomeScreen(),
    );
  }
}