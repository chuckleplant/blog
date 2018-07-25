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
    def initialize(site, base, dir, photo_url, album, previous_pic, next_pic, title, description)
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
      dir = site.config['photo_dir'] || 'photography'

      site.pages << PhotoList.new(site, site.source, File.join(dir), photos["photos"], "Photography")

      #Reference in site, used for sitemap
      photoSlugs = Array.new

      photos.each do |photo,details|
        #Iterate through array & return previous, current & next
        [nil, *details, nil].each_cons(3){|prev, curr, nxt|
          pic_album = curr["album"]
          photo_url = curr["img"]
          title = curr["title"]
          description = curr["description"]
          title_stub = title.strip.gsub(' ', '-').gsub(/[^\w-]/, '') #remove non-alpha and replace spaces with hyphens
          title_stub = pic_album+'/'+title_stub
          if(prev != nil)
            previous_pic = prev["title"].strip.gsub(' ', '-').gsub(/[^\w-]/, '')
          else
            previous_pic = ""
          end
          if(nxt != nil)
            next_pic = nxt["title"].strip.gsub(' ', '-').gsub(/[^\w-]/, '')
          else
            next_pic = ""
          end
          photoSlugs << photo_url
          site.pages << PhotoPage.new(site, site.source, File.join(dir, title_stub), photo_url, pic_album, previous_pic, next_pic, title, description)
        }
      end
      site.data['photoSlugs'] = photoSlugs

      ##Create a array containing all countries
      #countryArray = Array.new
      #photos.each do |photo,details|
      #  [nil, *details, nil].each_cons(3){|prev, curr, nxt|
      #    photoCountry = curr["country"]
      #    countryArray.push(photoCountry)
      #  }
      #end
      #countryArray = countryArray.uniq
#
      #countryArray.each do |name|
      #  photosPerCountry = Array.new
      #  countrySlug = name.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
      #  photos.each do |photo, details|
      #    [nil, *details, nil].each_cons(3){|prev, curr, nxt|
      #      if(curr["country"] == name)
      #        photosPerCountry.push(curr)
      #      end
      #    }
      #  end
#
      #  #Make page
      #  site.pages << PhotoList.new(site, site.source, File.join('photography', countrySlug), #photosPerCountry, name)
      #end
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
      @result = '<div id="gallery" style="display:none; margin-top: 20px; margin-bottom: 20px;">'
      #photos = YAML::load_file('_data/photos.yaml')
      photos = get_all_photos()
      photos.each do |photo, details|
        [nil, *details, nil].each_cons(3){|prev, curr, nxt|
        if(curr["album"] == text.strip)
            width, height = Dimensions.dimensions(Dir.pwd + '/images/photography/thumbnails/'+curr["img"]+'.jpg')
            @result = @result+'<div itemscope itemtype="http://schema.org/Photograph">
                                      <a target="_blank" itemprop="image" class="swipebox" title="'+curr["title"]+'" href="/photography/'+curr["album"]+'/'+curr["title"].strip.gsub(' ', '-').gsub(/[^\w-]/, '')+'/">
                                        <img  width="'+width.to_s+'" height="'+height.to_s+'" alt="'+curr["title"]+'" itemprop="thumbnailUrl" src="/images/photography/thumbnails/'+curr["img"]+'.jpg"/>
                                        <meta itemprop="name" content="'+curr["title"]+'" />
                                        <meta itemprop="isFamilyFriendly" content="true" />
                                        <div itemprop="creator" itemscope itemtype="http://schema.org/Person">
                                          <div itemprop="sameAs" href="https://chuckleplant.github.io/about">
                                            <meta itemprop="name" content="Sergio Basurco"/>
                                          </div>
                                        </div>
                                      </a>
                                    </div>'
          end
        }
      end
      @result = @result + '</div>'

      #If you want to configure each album gallery individually you can remove this script
      #and add it in the template/post directly.
      @result = @result + '<script>
                              window.onload=function(){
                                  $("#gallery").justifiedGallery({
                                      rowHeight : 180,
                                      maxRowHeight: 0,
                                      margins : 3,
                                      border : 0,
                                      fixedHeight: false,
                                      lastRow : \'nojustify\',
                                      captions: true,
                                      waitThumbnailsLoad: false
                                  });
                                  $("#gallery").fadeIn(500);
                              }
                          </script>'
    end

    def render(context)
      "#{@result}"
    end
  end
end
Liquid::Template.register_tag('includeGallery', Jekyll::IncludeGalleryTag)
