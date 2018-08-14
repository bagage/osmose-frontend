{{!mustache_delimiter}}
<div id="popup-{%error_id%}">
  <div class="bulle_msg">
    <div class="closebubble">
      <div class="help"><a target="popup_help" href='{%url_help%}#{%item%}' title="{{_('Help on OSM Wiki')}}">&nbsp;?&nbsp;</a></div>
      <div class="error-link"><a target="_blank" href="../error/{%error_id%}" title="{{_('Issue details')}}">&nbsp;E&nbsp;</a></div>
    </div>
    <div class="bulle_err">
      <b>{% title %}</b>
      <br>
      {%subtitle%}
    </div>
{%#elems%}
    <div class="bulle_elem">
  {%^infos%}
      <b><a target="_blank" href="{{main_website}}{%type%}/{%id%}" title="{{_('Show Object on {where}').format(where=main_website)}}">{%type%} {%id%}</a></b>
      <a href="#" onclick="window.open('http://rawedit.openstreetmap.fr/edit/{%type%}/{%id%}','rawedit','height=360,width=710');">rawedit</a>
  {%/infos%}
  {%#relation%}
      <a target="_blank" href="http://analyser.openstreetmap.fr/cgi-bin/index.py?relation={%id%}">analyse1</a>
      <a target="_blank" href="http://polygons.openstreetmap.fr/~osmbin/analyse-relation-open.py?{%id%}">analyse2</a>
  {%/relation%}
  {%#node%}
      <a href="http://localhost:8111/load_object?objects=n{%id%}" target="hiddenIframe" class="josm" title="{{_('Edit Object with {where}').format(where='JOSM')}}">josm</a>
  {%/node%}
  {%#way%}
      <a href="http://localhost:8111/load_object?objects=w{%id%}" target="hiddenIframe" class="josm" title="{{_('Edit Object with {where}').format(where='JOSM')}}">josm</a>
  {%/way%}
  {%#relation%}
      <a href="http://localhost:8111/import?url={{remote_url_read}}api/0.6/{%type%}/{%id%}/full" target="hiddenIframe" class="josm" title="{{_('Edit Object with {where}').format(where='JOSM')}}" onclick="$.get('http://localhost:8111/zoom?left={%minlon%}&bottom={%minlat%}&right={%maxlon%}&top={%maxlat%}'); return true;">josm</a>
  {%/relation%}
      <a href="#" class="editor_edit" data-type="{%type%}" data-id="{%id%}" data-error="{%error_id%}" title="{{_('Edit Object with {where}').format(where=_('online Osmose Editor'))}}">edit</a>
      <br>
  {%#fixes%}
      <div class="fix">
        <div class="fix_links">
            <a href="http://localhost:8111/import?url=http://{{website}}/api/0.2/error/{%error_id%}/fix/{%num%}" target="hiddenIframe" class="josm" title="{{_('Load the fix in {where}').format(where='JOSM')}}" onclick="$.get('http://localhost:8111/zoom?left={%minlon%}&bottom={%minlat%}&right={%maxlon%}&top={%maxlat%}'); return true;">fix-josm</a>
            <a href="#" class="editor_fix" data-type="{%type%}" data-id="{%id%}" data-error="{%error_id%}" data-fix="{%num%}" title="{{_('Load the fix in {where}').format(where=_('online Osmose Editor'))}}">fix-edit</a>
        </div>
    {%#add%}
        <div class="add"> + <b>{%k%}</b> =
          {%#vlink%}<a href="{%vlink%}" target="popup_tag2link">{%/vlink%}
          {%v%}
          {%#vlink%}</a>{%/vlink%}
        </div>
    {%/add%}
    {%#mod%}
        <div class="mod"> ~ <b>{%k%}</b> =
          {%#vlink%}<a href="{%vlink%}" target="popup_tag2link">{%/vlink%}
          {%v%}
          {%#vlink%}</a>{%/vlink%}
        </div>
    {%/mod%}
    {%#del%}
        <div class="del"> - <b>{%k%}</b></div>
    {%/del%}
      </div>
  {%/fixes%}
  {%#tags%}
      <b>{%k%}</b> =
      {%#vlink%}<a href="{%vlink%}" target="popup_tag2link">{%/vlink%}
      {%v%}
      {%#vlink%}</a>{%/vlink%}
      <br>
  {%/tags%}
    </div>
{%/elems%}
{%#new_elems%}
    <div class="bulle_elem">
      <div class="fix">
        <div class="fix_links">
          <a href="http://localhost:8111/import?url=http://{{website}}/api/0.2/error/{%error_id%}/fix/{%num%}" target="hiddenIframe" class="josm" title="{{_('Add the new object in {where}').format(where='JOSM')}}" onclick="$.get('http://localhost:8111/zoom?left={%minlon%}&bottom={%minlat%}&right={%maxlon%}&top={%maxlat%}'); return true;">fix-josm</a>
        </div>
  {%#add%}
        <div class="add"> + <b>{%k%}</b> =
          {%#vlink%}<a href="{%vlink%}" target="popup_tag2link">{%/vlink%}
          {%v%}
          {%#vlink%}</a>{%/vlink%}
        </div>
  {%/add%}
  {%#mod%}
        <div class="mod"> ~ <b>{%k%}</b> =
          {%#vlink%}<a href="{%vlink%}" target="popup_tag2link">{%/vlink%}
          {%v%}
          {%#vlink%}</a>{%/vlink%}
        </div>
  {%/mod%}
  {%#del%}
        <div class="del"> - <b>{%k%}</b></div>
  {%/del%}
      </div>
    </div>
{%/new_elems%}
  <span title="{{_('Report based on data from date')}}">{{_("Issue reported on: ")}} {%b_date%}</span>
  </div>
  <div class="bulle_verif">
    <a href="{{main_website}}?lat={%lat%}&lon={%lon%}&zoom=18" target="popup_osm" title="{{_('Show the area on {where}').format(where=main_website)}}">osm-show</a>
    <a href="{{main_website}}edit?lat={%lat%}&lon={%lon%}&zoom=18" target="_blank" title="{{_('Edit the area on {where}').format(where=main_website)}}">osm-edit</a>
    <a href="http://localhost:8111/load_and_zoom?left={%minlon%}&bottom={%minlat%}&right={%maxlon%}&top={%maxlat%}&select={%elems_id%}" target="hiddenIframe" class="josm" title="{{_('Edit the area on {where}').format(where='JOSM')}}">josm-zone</a>
  </div>
  <div class="bulle_maj">
    <b>{{_("change status")}} :</b>
    <a class="closePopup corrected" href="../api/0.2/error/{%error_id%}/done" target="hiddenIframe" title="{{_('After issue fixed on the OSM data, mark it as done. May also disapear automaticlay on next check if no more issue.')}}">{{_("corrected")}}</a>
    <a class="closePopup false_positive" href="../api/0.2/error/{%error_id%}/false" target="hiddenIframe" title="{{_('Report the issue as improper, if according to you is not an issue. The issue will not be displayed to anyone more.')}}">{{_("false positive")}}</a>
</div>

</div>
