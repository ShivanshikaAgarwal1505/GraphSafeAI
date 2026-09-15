import 'package:flutter/material.dart';

class RiskUtils {

  static Color color(
    double risk,
  ) {

    if (risk < 0.15) {
      return Colors.green;
    }

    if (risk < 0.25) {
      return Colors.orange;
    }

    return Colors.red;
  }

  static String label(
    double risk,
  ) {

    if (risk < 0.15) {
      return "LOW";
    }

    if (risk < 0.25) {
      return "MEDIUM";
    }

    return "HIGH";
  }
}