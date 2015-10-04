from toolchain import Recipe, shprint
from os.path import join
from os import getcwd
import sh


class LibSDL2Recipe(Recipe):
    version = "iOS-improvements"
    url = "https://bitbucket.org/slime73/sdl-experiments/get/{version}.tar.gz"
    library = "Xcode-iOS/SDL/build/Release-{arch.sdk}/libSDL2.a"
    include_dir = "include"
    pbx_frameworks = ["OpenGLES", "AudioToolbox", "QuartzCore", "CoreGraphics",
            "CoreMotion",]

    def prebuild_arch(self, arch):
        if self.has_marker("patched"):
            return

        self.apply_patch("uikit-transparent.patch")

        self.set_marker("patched")

    def build_arch(self, arch):
        shprint(sh.xcodebuild,
                "ONLY_ACTIVE_ARCH=NO",
                "ARCHS={}".format(arch.arch),
                "-sdk", arch.sdk,
                "-project", "Xcode-iOS/SDL/SDL.xcodeproj",
                "-target", "libSDL",
                "-configuration", "Release")


recipe = LibSDL2Recipe()

