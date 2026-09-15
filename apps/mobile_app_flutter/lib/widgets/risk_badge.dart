import 'package:flutter/material.dart';

import '../core/utils/risk_utils.dart';

class RiskBadge extends StatelessWidget {
  final double risk;

  const RiskBadge({
    super.key,
    required this.risk,
  });

  @override
  Widget build(BuildContext context) {
    return Chip(
      backgroundColor:
          RiskUtils.color(risk),

      label: Text(
        '${RiskUtils.label(risk)} (${risk.toStringAsFixed(3)})',

        style: const TextStyle(
          color: Colors.white,
        ),
      ),
    );
  }
}