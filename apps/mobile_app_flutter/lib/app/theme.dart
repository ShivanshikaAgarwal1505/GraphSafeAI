import 'package:flutter/material.dart';

class AppColors {

  static const primary =
      Color(0xFF0066FF);

  static const accent =
      Color.fromARGB(255, 165, 49, 69);

  static const warning =
      Color(0xFFFFB300);

  static const danger =
      Color(0xFFE53935);

  static const background =
      Color(0xFFF8F9FB);
}

class AppTheme {

  static ThemeData get light {

    return ThemeData(

      useMaterial3: true,

      scaffoldBackgroundColor:
          AppColors.background,

      colorScheme:
          ColorScheme.fromSeed(
        seedColor:
            AppColors.primary,
      ),

      navigationBarTheme:
          const NavigationBarThemeData(

        indicatorColor:
            AppColors.primary,
      ),

      floatingActionButtonTheme:
          const FloatingActionButtonThemeData(

        backgroundColor:
            AppColors.primary,

        foregroundColor:
            Colors.white,
      ),
    );
  }
}