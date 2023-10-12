module Jekyll
    module FontTagFilter
      def text_color(input, color)
        "<font class='post-colored-text' color='#{color}'>#{input}</font>"
      end
    end
  end
  
  Liquid::Template.register_filter(Jekyll::FontTagFilter)
  