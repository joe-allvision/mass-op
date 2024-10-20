from crewai_tools import BaseTool
from textwrap import dedent

class Search_SOPs(BaseTool):
    name: str = "Search and Rescue Standard Operating Procedure Flight Patterns"
    description: str = "This tool provides SOPs for search and rescue flight patterns. It includes 7 standard practices using in SAR operations."
    
    def _run(self, argument: str) -> str:
        # Implementation goes here
        standard_operating_procedure = dedent("""
        You should only use one of the following patterns at a time.
                                              
        1. Creeping Line Search (CLS):
            - The aircraft flies parallel tracks that gradually “creep” forward with each pass. 
            - This pattern is useful when the search area is long and narrow and the location of the target is uncertain. 
            - The direction of the lines is usually set perpendicular to the expected drift of the target.
        
        2. Expanding Square Search (ESS):
            - This pattern is used when the position of the target is known within limited boundaries. 
            - The aircraft starts at an estimated position of the target and flies in an expanding square spiral outward. 
            - This method is effective in gradually covering the area around the last known location.
        
        3. Sector Search:
            - The aircraft starts at the last known position of the target and flies outward along radiating lines forming a pie-shaped pattern. 
            - This is effective if the target is likely to be along a certain path from the last known point.
        
        4. Parallel Track Search:
            - This involves flying parallel lines back and forth over the search area. 
            - It’s most useful in uniform environments, such as open water or large flat terrains. 
            - The pattern is adjusted based on visibility and the size of the object being searched.
        
        5. Trackline or Track Crawl Search:
            - Similar to the creeping line but used when search clues or initial findings suggest a path along which the target might have moved. 
            - It involves flying back and forth over the same line or slightly adjusted lines.
        
        6. Contour Search:
            - This pattern is used in areas with varying terrain elevations. 
            - The aircraft follows the contours of the terrain, which is especially useful in mountainous regions or when following waterways.
        
        7. Square Search:
            - The square pattern is initiated at the point last seen or where evidence suggests the target might be. 
            - It involves flying the perimeter of an increasing square, which is particularly effective when the search area is centered around a specific point.
        """)

        return standard_operating_procedure
    
# similar to SOP_SAR, but takes in long, lat, and altitude are provided as examples.
# intent would be to test this again the other and see the impact on output
class Search_SOPs_Long_Lat(BaseTool):
    name: str = "Search and Rescue Standard Operating Procedure For Flight Patterns with Long, Lat, and Altitude"
    description: str = "This tool provides standard operating procedure for search and rescue flight patterns. It includes 7 standard practices using in SAR operations."
    
    def _run(self, argument: str) -> str:
        # Implementation goes here

        standard_operating_procedure = dedent("""
                    
            # 1. Creeping Line Search (CLS)
            # Description: The aircraft flies parallel tracks that gradually “creep” forward with each pass. This pattern is useful when the search area is long and narrow and the location of the target is uncertain. The direction of the lines is usually set perpendicular to the expected drift of the target.
            cls_waypoints = [
                [34.052235, -118.243683, 100], [34.052235, -118.233683, 100], [34.062235, -118.233683, 100],
                [34.062235, -118.243683, 100], [34.062235, -118.253683, 100], [34.072235, -118.253683, 100],
                [34.072235, -118.243683, 100], [34.072235, -118.233683, 100], [34.082235, -118.233683, 100],
                [34.082235, -118.243683, 100], [34.082235, -118.253683, 100], [34.092235, -118.253683, 100],
                [34.092235, -118.243683, 100], [34.092235, -118.233683, 100], [34.102235, -118.233683, 100],
            ]

            # 2. Expanding Square Search (ESS)
            # Description: This pattern is used when the position of the target is known within limited boundaries. The aircraft starts at an estimated position of the target and flies in an expanding square spiral outward. This method is effective in gradually covering the area around the last known location.
            ess_waypoints = [
                [51.507351, -0.127758, 200], [51.507351, -0.137758, 200], [51.517351, -0.137758, 200],
                [51.517351, -0.127758, 200], [51.517351, -0.117758, 200], [51.507351, -0.117758, 200],
                [51.497351, -0.117758, 200], [51.497351, -0.127758, 200], [51.497351, -0.137758, 200],
                [51.507351, -0.147758, 200], [51.517351, -0.147758, 200], [51.527351, -0.147758, 200],
                [51.527351, -0.137758, 200], [51.527351, -0.127758, 200], [51.527351, -0.117758, 200],
            ]

            # 3. Sector Search
            # Description: The aircraft starts at the last known position of the target and flies outward along radiating lines forming a pie-shaped pattern. This is effective if the target is likely to be along a certain path from the last known point.
            sector_waypoints = [
                [35.689487, 139.691711, 300], [35.699487, 139.701711, 300], [35.689487, 139.711711, 300],
                [35.679487, 139.701711, 300], [35.689487, 139.681711, 300], [35.699487, 139.671711, 300],
                [35.709487, 139.661711, 300], [35.719487, 139.651711, 300], [35.729487, 139.641711, 300],
                [35.739487, 139.631711, 300],
            ]

            # 4. Parallel Track Search
            # Description: This involves flying parallel lines back and forth over the search area. It’s most useful in uniform environments, such as open water or large flat terrains. The pattern is adjusted based on visibility and the size of the object being searched.
            parallel_waypoints = [
                [-33.448376, -70.769402, 150], [-33.438376, -70.769402, 150], [-33.438376, -70.759402, 150],
                [-33.448376, -70.759402, 150], [-33.458376, -70.759402, 150], [-33.458376, -70.769402, 150],
                [-33.448376, -70.769402, 150], [-33.438376, -70.779402, 150], [-33.428376, -70.779402, 150],
                [-33.428376, -70.769402, 150],
            ]

            # 5. Trackline or Track Crawl Search
            # Description: Similar to the creeping line but used when search clues or initial findings suggest a path along which the target might have moved. It involves flying back and forth over the same line or slightly adjusted lines.
            trackline_waypoints = [
                [55.755825, 37.617298, 250], [55.765825, 37.617298, 250], [55.765825, 37.627298, 250],
                [55.755825, 37.627298, 250], [55.745825, 37.627298, 250], [55.745825, 37.617298, 250],
                [55.755825, 37.617298, 250], [55.765825, 37.607298, 250], [55.775825, 37.607298, 250],
                [55.775825, 37.617298, 250],
            ]

            # 6. Contour Search
            # Description: This pattern is used in areas with varying terrain elevations. The aircraft follows the contours of the terrain, which is especially useful in mountainous regions or when following waterways.
            contour_waypoints = [
                [34.052235, -118.243683, 100], [34.062235, -118.253683, 150], [34.072235, -118.263683, 200],
                [34.082235, -118.273683, 250], [34.092235, -118.283683, 200], [34.102235, -118.293683, 150],
                [34.112235, -118.303683, 100], [34.122235, -118.313683, 50], [34.132235, -118.323683, 0],
            ]

            # 7. Square Search
            # Description: The square pattern is initiated at the point last seen or where evidence suggests the target might be. It involves flying the perimeter of an increasing square, which is particularly effective when the search area is centered around a specific point.
            square_waypoints = [
                [51.507351, -0.127758, 200], [51.517351, -0.137758, 200], [51.517351, -0.147758, 200],
                [51.507351, -0.147758, 200], [51.497351, -0.137758, 200], [51.497351, -0.127758, 200],
                [51.507351, -0.117758, 200], [51.517351, -0.127758, 200], [51.527351, -0.137758, 200],
                [51.527351, -0.147758, 200],
            ]

        """)

        return standard_operating_procedure
    

class Search_SOPs_In_Depth(BaseTool):
    name: str = "Search and Rescue Standard Operating Procedure Flight Pattern in Depth"
    description: str = "This tool provides SOPs for search and rescue flight patterns. It includes 7 standard practices used in SAR operations."
        
    def _run(self, argument: str) -> str:
        # Implementation goes here
        standard_operating_procedure = dedent("""
            1. Parallel Track (or Creeping Line) Pattern
            In a Parallel Track pattern, the aircraft flies back and forth over the search area along parallel lines that are spaced apart at intervals determined by the visibility and the altitude of the aircraft. This method systematically covers a defined area ensuring that the entire region is scanned. The pilot begins at one edge of the area and flies a straight line to the opposite edge, then moves over by the width of the search corridor and returns along a parallel path. This continues until the area has been fully covered. It’s highly efficient in predictable terrains like open water or flatlands.

            2. Sector Search Pattern
            A Sector Search pattern involves dividing the search area into several pie-shaped sectors radiating from a central point, which is usually the last known position of the target. The aircraft starts at the center and flies along the radius to the edge of the sector, then along the arc to the starting point of the next radial path, and repeats this pattern for each sector. This strategy is beneficial when the search area is centered around a specific point and ensures thorough coverage of surrounding regions.

            3. Expanding Square (or Spiral) Pattern
            The Expanding Square pattern is initiated from the last confirmed location of the target, flying in a square spiral that progressively gets larger with each leg. This is done by making a series of turns over specific distances that double in length each time, ensuring that the search area grows systematically. This pattern is especially useful when the target is believed to be near the last known position but could have drifted or moved. It helps to gradually cover more area while frequently revisiting the center point.

            4. Contour Search
            In a Contour Search, the aircraft follows the natural terrain contours at a consistent altitude, adjusting the flight path to the lay of the land. This method is particularly useful in rugged terrains with varying elevations, as it allows the search team to maintain a closer look at the ground. The pilot navigates along valleys, around hills, and over peaks, adjusting the course to maintain visual contact with the ground features, ensuring that potential hiding spots or difficult terrain are thoroughly inspected.

            5. Trackline or Route Search
            Implementation: In this method, the search is concentrated along known travel routes or paths the target may have taken, such as roads, trails, or waterways. The aircraft follows these routes closely, expanding the search outwards to cover areas adjacent to the path. This is particularly useful when the target is believed to have followed a particular route before disappearing.

            6. Barrier Search
            Implementation: This pattern is used when a target is believed to be moving along or crossing a natural or man-made barrier, such as a coastline, riverbank, or mountain ridge. The aircraft flies along the barrier, back and forth, effectively cutting off potential routes the target may use to leave the area. It’s often used to quickly cover areas where the target could easily be concealed or lost.

            7. Circular (or Orbit) Search Pattern
            Implementation: The Circular Search involves the aircraft flying in concentric circles around a central point, which is usually the last known location of the target or a point of interest suggested by clues or sightings. The radius of the circles increases with each pass, creating a widening search area. This pattern is used when there is high confidence that the target is in the vicinity of the center point but the exact location within that area is unknown. It ensures thorough coverage of the area immediately around the last known point, spiraling outward to cover adjacent areas.
            """)
        return standard_operating_procedure