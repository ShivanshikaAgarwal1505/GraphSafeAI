import 'package:flutter/material.dart';

import '../navigation/main_navigation.dart';
import 'theme.dart';
class GraphSafeAIApp
    extends StatelessWidget {

  const GraphSafeAIApp({
    super.key,
  });

  @override
  Widget build(BuildContext context) {

    return MaterialApp(

      debugShowCheckedModeBanner:
          false,

      title: 'GraphSafeAI',

      theme: AppTheme.light,

      home:
          const MainNavigation(),
    );
  }
}