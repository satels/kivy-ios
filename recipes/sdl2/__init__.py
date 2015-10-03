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
            "CoreMotion",]#"GoogleMobileAds"]

    def prebuild_arch(self, arch):
        if self.has_marker("patched"):
            return

        # ads_framework_path = join(getcwd(), "GoogleMobileAds.framework")
        #
        # self.copy_folder("GoogleMobileAds.framework", ads_framework_path)

        self.apply_patch("uikit-transparent.patch")
        # self.apply_patch("uikit-admob.patch")
        #
        # from mod_pbxproj import XcodeProject
        #
        # project = XcodeProject.Load('Xcode-iOS/SDL/SDL.xcodeproj/project.pbxproj')
        #
        # print 'GoogleMobileADS:', ads_framework_path
        #
        # project.add_file_if_doesnt_exist(ads_framework_path, tree="SOURCE_ROOT")
        #
        # project.add_flags("OTHER_LDFLAGS", ["-miphoneos-version-min=6.0.0",])
        #
        # print 'SDL XCODE is modified', project.modified
        #
        # if project.modified:
        #     project.backup()
        #     project.save()

        self.set_marker("patched")

    def build_arch(self, arch):
        shprint(sh.xcodebuild,
                "ONLY_ACTIVE_ARCH=NO",
                "ARCHS={}".format(arch.arch),
                # "CLANG_ENABLE_MODULES=YES",
                "-sdk", arch.sdk,
                "-project", "Xcode-iOS/SDL/SDL.xcodeproj",
                "-target", "libSDL",
                "-configuration", "Release")


recipe = LibSDL2Recipe()

