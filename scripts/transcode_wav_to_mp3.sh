#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Transcode WAVs to Spotify-friendly MP3 (128k, mono, 44.1kHz).

Usage:
  scripts/transcode_wav_to_mp3.sh [options]

Options:
  -i, --input DIR    Input directory containing .wav files (default: audio)
  -o, --output DIR   Output directory for .mp3 files (default: same as input)
  -f, --force        Overwrite existing .mp3 files
  -h, --help         Show this help

Environment overrides:
  BITRATE=128k  SAMPLE_RATE=44100  CHANNELS=1
USAGE
}

in_dir="audio"
out_dir=""
force=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -i|--input)
      in_dir="$2"
      shift 2
      ;;
    -o|--output)
      out_dir="$2"
      shift 2
      ;;
    -f|--force)
      force=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ -z "${out_dir}" ]]; then
  out_dir="${in_dir}"
fi

if [[ ! -d "${in_dir}" ]]; then
  echo "Input directory not found: ${in_dir}" >&2
  exit 1
fi

mkdir -p "${out_dir}"

bitrate="${BITRATE:-128k}"
sample_rate="${SAMPLE_RATE:-44100}"
channels="${CHANNELS:-1}"

overwrite_flag="-n"
if [[ "${force}" -eq 1 ]]; then
  overwrite_flag="-y"
fi

shopt -s nullglob
wav_files=("${in_dir}"/*.wav)
if [[ ${#wav_files[@]} -eq 0 ]]; then
  echo "No .wav files found in ${in_dir}" >&2
  exit 1
fi

for f in "${wav_files[@]}"; do
  base="$(basename "${f%.wav}")"
  out="${out_dir}/${base}.mp3"

  if [[ -f "${out}" && "${force}" -ne 1 ]]; then
    echo "Skipping existing: ${out}"
    continue
  fi

  ffmpeg "${overwrite_flag}" -i "${f}" \
    -c:a libmp3lame -b:a "${bitrate}" -ac "${channels}" -ar "${sample_rate}" \
    "${out}"
done
