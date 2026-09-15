import 'package:flutter/material.dart';

import '../../../app/theme.dart';

class SearchPanel extends StatelessWidget {
  const SearchPanel({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      elevation: 6,
      borderRadius:
          BorderRadius.circular(32),

      child: TextField(
        decoration: InputDecoration(
          border: InputBorder.none,

          enabledBorder:
              OutlineInputBorder(
            borderRadius:
                BorderRadius.circular(
                    32),
            borderSide:
                BorderSide.none,
          ),

          focusedBorder:
              OutlineInputBorder(
            borderRadius:
                BorderRadius.circular(
                    32),
            borderSide:
                const BorderSide(
              color:
                  AppColors.primary,
              width: 2,
            ),
          ),

          isDense: true,

          contentPadding:
              const EdgeInsets.symmetric(
            horizontal: 18,
            vertical: 14,
          ),

          prefixIcon: const Icon(
            Icons.search,
            color: AppColors.primary,
          ),

          hintText:
              'Where are you going?',
        ),
      ),
    );
  }
}