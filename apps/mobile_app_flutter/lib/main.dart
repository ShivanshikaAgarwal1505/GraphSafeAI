import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'app/app.dart';
import 'features/navigation/providers/navigation_provider.dart';
import 'features/reports/providers/reports_provider.dart';
import 'features/location/providers/location_provider.dart';
import 'features/search/providers/search_provider.dart';
import 'features/auth/providers/auth_provider.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => NavigationProvider(),
        ),

        ChangeNotifierProvider(
          create: (_) => ReportsProvider(),
        ),

        ChangeNotifierProvider(
          create: (_) => LocationProvider(),
        ),
        
        ChangeNotifierProvider(
          create: (_) => SearchProvider(),
        ),

        ChangeNotifierProvider(
          create: (_) => AuthProvider()
          ..initialize(),
        ),
      ],
      child: const GraphSafeAIApp(),
    ),
  );
}