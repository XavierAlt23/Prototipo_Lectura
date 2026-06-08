#!/bin/bash
# Genera reportes de evaluacion.

set -e

cd ml
python evaluation/generate_comparison_report.py
