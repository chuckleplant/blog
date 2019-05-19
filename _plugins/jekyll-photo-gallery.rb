#Jekyll-Photo-Gallery generates a HTML page for every photo specified in _data/photos.yaml
#Author: Theo Winter (https://github.com/aerobless)
# Mods by: Sergio Basurco & Julian Ramos
require 'find'
require 'yaml'
require 'dimensions'

def get_all_photos()
  allPics = []
  Dir.glob('_data/photos/*.yaml') do |y_file, index|
    auxHash = YAML.load_file(y_file)
    tmpHash = auxHash["photos"]
    allPics.push(*tmpHash)
  end
  picsObj = {"photos" => allPics}
  return picsObj
end

module Jekyll
  class PhotoPage < Page
    def initialize(site, base, dir, photo_url, album, previous_pic, next_pic, title, description, latitude, longitude, date_time_original, cam_model, lens_model, exposure, f_number, iso, focal_length, user_comment)
      @site = site
      @base = base
      @dir = dir
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'photo.html')
      self.data['photo_url'] = photo_url
      self.data['album'] = album
      self.data['previous_pic'] = previous_pic
      self.data['next_pic'] = next_pic
      self.data['title'] = title
      self.data['description'] = description
      self.data['comments'] = true
      self.data['disqus_identifier'] = album+ '-' +title
      self.data['latitude'] = latitude
      self.data['longitude']= longitude
      self.data['date_time_original'] = date_time_original
      self.data['cam_model'] = cam_model
      self.data['lens_model'] = lens_model
      self.data['exposure'] = exposure
      self.data['f_number'] = f_number
      self.data['iso'] = iso
      self.data['focal_length'] = focal_length
      self.data['user_comment'] = user_comment

    end
  end

  class PhotoList < Page
    def initialize(site, base, dir, photolist, title)
      @site = site
      @base = base
      @dir = dir
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'photoIndex.html')
      self.data['photolist'] = photolist
      self.data['title'] = title
    end
  end

  

  class PhotoPageGenerator < Generator
    safe true

    def generate(site)
      photos = get_all_photos()
      dir = site.config['photo_dir']
      photos.each do |photo,details|
        #Iterate through array & return previous, current & next
        [nil, *details, nil].each_cons(3){|prev, curr, nxt|
          pic_album = curr["album"]
          photo_url = curr["img"]
          latitude = curr["latitude"]
          longitude = curr["longitude"]
          date_time_original = curr["date_time_original"]
          cam_model = curr["cam_model"]
          lens_model = curr["lens_model"]
          exposure = curr["exposure"]
          f_number = curr["f_number"]
          iso = curr["iso"]
          focal_length = curr["focal_length"]
          title = curr["title"]
          description = curr["description"]
          user_comment = curr["user_comment"]

          title_stub = title.strip.gsub(' ', '-').gsub(/[^\w-]/, '') #remove non-alpha and replace spaces with hyphens
          title_stub = pic_album+'/'+title_stub
          if(prev != nil && prev["album"] == curr["album"])
            previous_pic = prev["title"].strip.gsub(' ', '-').gsub(/[^\w-]/, '')
          else
            previous_pic = ""
          end

          if(nxt != nil  && nxt["album"] == curr["album"])
            next_pic = nxt["title"].strip.gsub(' ', '-').gsub(/[^\w-]/, '')
          else
            next_pic = ""
          end
          site.pages << PhotoPage.new(site, site.source, File.join(dir, title_stub), photo_url, pic_album, previous_pic, next_pic, title, description, latitude, longitude, date_time_original, cam_model, lens_model, exposure, f_number, iso, focal_length, user_comment)
        }
      end
    end
  end
end

module TextFilter
  def toStub(input)
    input.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
  end
end



Liquid::Template.register_filter(TextFilter)

module Jekyll
  class IncludeGalleryTag < Liquid::Tag


    def initialize(tag_name, text, tokens)
      super
      @result = '<div id="pig"></div>'
      @result = @result + ' <script src="/js/plugins/pig/src/pig.min.js"></script>'

      @result = @result + ' <script>
                              var imageData = ['
#
      photos = get_all_photos()
      photos.each do |photo, details|
        [nil, *details, nil].each_cons(3){|prev, curr, nxt|
          if(curr["album"] == text.strip)
            @result = @result+'{filename: "'+curr["img"]+'", aspectRatio: '+curr["aspect"].to_s+', url: "'+ '/img/albums/' + curr["album"] +'/'+ curr["title"].strip.gsub(' ', '-').gsub(/[^\w-]/, '')+'/"},'
          end
        }
      end
                       
      @result = @result + '];
                              var options = {
                                urlForSize: function(filename, size) {
                                  return '"'"'/img/'"'"' + size + '"'"'/'"'"' + filename;
                                },
                                figureTagName: "a",
                                transitionSpeed: 500,
                                getMinAspectRatio: function(lastWindowWidth) {
                                if (lastWindowWidth <= 640)  // Phones
                                  return 1;
                                else if (lastWindowWidth <= 1280)  // Tablets
                                  return 3;
                                else if (lastWindowWidth <= 1920)  // Laptops
                                  return 4;
                                return 5;  // Large desktops
                              },
                                spaceBetweenImages: 3,
                                getImageSize: function(lastWindowWidth) {
                                  return 250;
                                }
                                // ...
                              };
                          
                              var pig = new Pig(imageData, options).enable();
                            </script>'
    end

    def render(context)
      "#{@result}"
    end
  end
end

Liquid::Template.register_tag('includeGallery', Jekyll::IncludeGalleryTag)
