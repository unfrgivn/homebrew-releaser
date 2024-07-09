# typed: true
# frozen_string_literal: true

# This file was generated by Homebrew Releaser. DO NOT EDIT.
class TestGenerateFormula < Formula
  

  desc "Tool to release scripts, binaries, and executables to github"
  homepage "https://github.com/Justintime50/test-generate-formula"
  url "https://github.com/Justintime50/test-generate-formula/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  depends_on "bash" => :build
  depends_on "gcc"

  def install
    bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"
  end

  test do
    assert_match("my script output", shell_output("my-script-command"))
  end
end
